from qgis.PyQt.QtCore import QSettings
from qgis.utils import iface


def xyz_exists(name: str) -> bool:
    s = QSettings()
    return s.contains(f"qgis/connections-xyz/{name}/url")


def wms_exists(name: str) -> bool:
    s = QSettings()
    return s.contains(f"qgis/connections-wms/{name}/url")


def ensure_xyz(name, url, zmin=0, zmax=19):
    if not xyz_exists(name):
        print(f"Creating XYZ {name}")
    else:
        print(f"Updating XYZ {name}")

    s = QSettings()
    base = f"qgis/connections-xyz/{name}"
    s.setValue(f"{base}/url", url)
    s.setValue(f"{base}/zmin", zmin)
    s.setValue(f"{base}/zmax", zmax)
    s.setValue(f"{base}/hidden", False)


def ensure_wms(name, url):
    if not wms_exists(name):
        print(f"Creating WMS {name}")
    else:
        print(f"Updating WMS {name}")

    s = QSettings()
    base = f"qgis/connections-wms/{name}"
    s.setValue(f"{base}/url", url)
    s.setValue(f"{base}/hidden", False)


# WMS layers to be added:
# Europe, Copernicus Urban Atlas (EEA)
# https://image.discomap.eea.europa.eu/arcgis/services/UrbanAtlas/UA_UrbanAtlas_2018/MapServer/WMSServer
# Europe, Corine Land Cover 2018 (EEA)
# https://image.discomap.eea.europa.eu/arcgis/services/Corine/CLC2018_WM/MapServer/WMSServer
# Europe, Coastal Zones Land Cover Land Use 2018 (EEA)
# https://image.discomap.eea.europa.eu/arcgis/services/CoastalZones/CZ_CoastalZones_2018/MapServer/WMSServer
# XYZ layers to be added:

# OpenTopoMap
# https://tile.opentopomap.org/{z}/{x}/{y}.png
# Google Dynamic World
# https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}
# CartoDB Dark Matter
# https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png
ensure_wms(
    "Copernicus Urban Atlas",
    "https://image.discomap.eea.europa.eu/arcgis/services/UrbanAtlas/UA_UrbanAtlas_2018/MapServer/WMSServer",
)
ensure_wms(
    "Corine Land Cover 2018",
    "https://image.discomap.eea.europa.eu/arcgis/services/Corine/CLC2018_WM/MapServer/WMSServer",
)
ensure_wms(
    "Coastal Zones Land Cover Land Use 2018",
    "https://image.discomap.eea.europa.eu/arcgis/services/CoastalZones/CZ_CoastalZones_2018/MapServer/WMSServer",
)
ensure_xyz("OpenTopoMap", "https://tile.opentopomap.org/{z}/{x}/{y}.png", 0, 17)
ensure_xyz(
    "Google Dynamic World", "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", 0, 20
)
ensure_xyz(
    "CartoDB Dark Matter",
    "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
    0,
    19,
)


iface.browserModel().refresh()
