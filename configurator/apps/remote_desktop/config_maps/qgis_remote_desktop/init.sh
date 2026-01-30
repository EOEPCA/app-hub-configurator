echo "Initializing remote desktop environment..."

mkdir -p /workspace/.local/share/QGIS/QGIS3/

chmod -R 700 /workspace/.local

cat > /workspace/.local/share/QGIS/QGIS3/startup.py <<'EOF'
from qgis.PyQt.QtCore import QSettings, QTimer
from qgis.core import QgsProviderRegistry


def xyz_exists(name: str) -> bool:
    s = QSettings()
    return s.contains(f"qgis/connections-xyz/{name}/url")


def wms_exists(name: str) -> bool:
    s = QSettings()
    return s.contains(f"qgis/connections-wms/{name}/url")


def ensure_xyz(name: str, url: str, zmin: int = 0, zmax: int = 19, hidden: bool = False):
    if not xyz_exists(name):
        print(f"[startup] Creating XYZ: {name}")
    else:
        print(f"[startup] Updating XYZ: {name}")

    s = QSettings()
    base = f"qgis/connections-xyz/{name}"
    s.setValue(f"{base}/url", url)
    s.setValue(f"{base}/zmin", zmin)
    s.setValue(f"{base}/zmax", zmax)
    s.setValue(f"{base}/hidden", hidden)


def ensure_wms(name: str, url: str, hidden: bool = False):
    if not wms_exists(name):
        print(f"[startup] Creating WMS: {name}")
    else:
        print(f"[startup] Updating WMS: {name}")

    s = QSettings()
    base = f"qgis/connections-wms/{name}"
    s.setValue(f"{base}/url", url)
    s.setValue(f"{base}/hidden", hidden)


def _reload_provider_connections(provider_key: str):
    """
    Force QGIS to reload connection definitions for a provider.
    This is what makes XYZ/WMS appear immediately without restart.
    """
    md = QgsProviderRegistry.instance().providerMetadata(provider_key)
    if not md:
        print(f"[startup] Provider metadata not found: {provider_key}")
        return

    cm = md.connectionManager()
    if not cm:
        print(f"[startup] No connection manager for provider: {provider_key}")
        return

    cm.reloadConnections()
    print(f"[startup] Reloaded connections for provider: {provider_key}")


def _refresh_browser():
    try:
        from qgis.utils import iface
        iface.browserModel().refresh()
        print("[startup] Browser model refreshed")
    except Exception as e:
        print(f"[startup] Browser refresh skipped: {e}")


def apply_standard_connections():
    # ---- WMS ----
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

    # ---- XYZ ----
    ensure_xyz("OpenTopoMap", "https://tile.opentopomap.org/{z}/{x}/{y}.png", 0, 17)
    ensure_xyz("Google Dynamic World", "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}", 0, 20)
    ensure_xyz("CartoDB Dark Matter", "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png", 0, 19)

    # force reload of provider connections
    _reload_provider_connections("wms")
    _reload_provider_connections("xyz")

    # refresh browser
    _refresh_browser()


# Run slightly later: startup.py can run before iface/providers are fully ready
QTimer.singleShot(2000, apply_standard_connections)

EOF