echo "Initializing remote desktop environment..."

mkdir -p /workspace/.local/share/QGIS/QGIS3/

chmod -R 700 /workspace/.local
conda activate env_qgis
cat > /workspace/.local/share/QGIS/QGIS3/startup.py <<'EOF'
from qgis.PyQt.QtCore import QSettings, QTimer

def xyz_exists(name: str) -> bool:
    s = QSettings()
    return s.contains(f"qgis/connections-xyz/{name}/url")

def wms_exists(name: str) -> bool:
    s = QSettings()
    return s.contains(f"qgis/connections-wms/{name}/url")

def ensure_xyz(name: str, url: str, zmin: int = 0, zmax: int = 19, hidden: bool = False):
    print(f"[startup] {'Creating' if not xyz_exists(name) else 'Updating'} XYZ: {name}")
    s = QSettings()
    base = f"qgis/connections-xyz/{name}"
    s.setValue(f"{base}/url", url)
    s.setValue(f"{base}/zmin", zmin)
    s.setValue(f"{base}/zmax", zmax)
    s.setValue(f"{base}/hidden", hidden)

def ensure_wms(name: str, url: str, hidden: bool = False):
    print(f"[startup] {'Creating' if not wms_exists(name) else 'Updating'} WMS: {name}")
    s = QSettings()
    base = f"qgis/connections-wms/{name}"
    s.setValue(f"{base}/url", url)
    s.setValue(f"{base}/hidden", hidden)

def ensure_stac():
    try:
        from qgis.core import QgsStacConnection, QgsHttpHeaders
        stac_name = "eoresults-stac"
        existing = QgsStacConnection.connectionList()
        if stac_name not in existing:
            print(f"[startup] Creating STAC connection: {stac_name}")
            headers = QgsHttpHeaders({"referer": "https://eoresults.esa.int/stac"})
            stac_data = QgsStacConnection.Data()
            stac_data.name = stac_name
            stac_data.url = "https://eoresults.esa.int/stac"
            stac_data.username = ""
            stac_data.password = ""
            stac_data.authCfg = ""
            stac_data.httpHeaders = headers
            QgsStacConnection.addConnection(stac_name, stac_data)
            QgsStacConnection.setSelectedConnection(stac_name)
            print(f"[startup] STAC connection added: {stac_name}")
        else:
            print(f"[startup] STAC connection already exists: {stac_name}")
    except Exception as e:
        print(f"[startup] STAC connection setup skipped: {e}")

def _refresh_browser():
    try:
        from qgis.utils import iface
        iface.browserModel().refresh()
        print("[startup] Browser model refreshed")
    except Exception as e:
        print(f"[startup] Browser refresh skipped: {e}")

def apply_standard_connections():
    # WMS
    ensure_wms("Copernicus Urban Atlas",
               "https://image.discomap.eea.europa.eu/arcgis/services/UrbanAtlas/UA_UrbanAtlas_2018/MapServer/WMSServer")
    ensure_wms("Corine Land Cover 2018",
               "https://image.discomap.eea.europa.eu/arcgis/services/Corine/CLC2018_WM/MapServer/WMSServer")
    ensure_wms("Coastal Zones Land Cover Land Use 2018",
               "https://image.discomap.eea.europa.eu/arcgis/services/CoastalZones/CZ_CoastalZones_2018/MapServer/WMSServer")

    # XYZ
    ensure_xyz("OpenTopoMap", "https://tile.opentopomap.org/{z}/{x}/{y}.png", 0, 17)
    ensure_xyz("Google Dynamic World", "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", 0, 20)
    ensure_xyz("CartoDB Dark Matter", "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png", 0, 19)

    # STAC
    ensure_stac()

    # Refresh browser a few times (sometimes needed)
    _refresh_browser()
    QTimer.singleShot(1500, _refresh_browser)
    QTimer.singleShot(4000, _refresh_browser)

    print("[startup] NOTE: provider connection reload API not available in this build; "
          "XYZ/WMS/STAC may only appear after restart.")

QTimer.singleShot(2000, apply_standard_connections)

EOF
