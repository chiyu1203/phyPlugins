
# You can also put your plugins in ~/.phy/plugins/.

from pathlib import Path

c = get_config()
c.Plugins.dirs = [str(Path.home() / ".phy" / "plugins")]
c.TemplateGUI.plugins = ['qualityMetricsPlugin', 'removeColumnsPlugin', 'clusterViewStylingPlugin']
