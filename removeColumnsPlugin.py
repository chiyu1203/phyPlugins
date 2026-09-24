# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 14:30:21 2020

@author: Julie

Modified on Thu Sep 24 2026
Due to an error related to different number between cluster ID and template ID. 
@author: Chiyu Lee and GPT-6 Sol Max 
"""
# import from plugins/custom_columns.py
from phy import IPlugin, connect
import numpy as np
"""only keep some columns in cluster view."""

class removeColumnsPlugin(IPlugin):
    def attach_to_controller(self, controller):
        # qualityMetricsPlugin registers this metric first. Replace its function
        # before phy constructs the supervisor and computes the cluster table.
        def spatial_decay_for_cluster(cluster_id):
            template_id = controller.get_template_for_cluster(cluster_id)
            if template_id is None:
                return float("nan")

            waveforms = controller.model.get_template_waveforms(template_id)
            if waveforms is None or np.size(waveforms) == 0:
                return float("nan")

            troughs = np.min(waveforms, axis=0)
            magnitudes = np.abs(troughs)
            smallest = np.min(magnitudes)
            return float(np.max(magnitudes) / smallest) if smallest > 0 else float("nan")

        controller.cluster_metrics["spatDeK"] = controller.context.memcache(
            spatial_decay_for_cluster
        )

        @connect(sender=controller)
        def on_controller_ready(sender):
            # '%missing' is omitted: the original qualityMetricsPlugin leaves
            # its calculation commented out, so it does not define that metric.
            controller.supervisor.columns = [
                "id", "ch", "sh", "n_spikes", "numRPV/numSpikes",
                "contamEstimate", "spatDeK", "fr", "amp",
            ]

