"""Initialize the az_storage subpackage of cdh_dav_python package"""
# allow absolute import from the root folder
# whatever its name is.
import sys  # don't remove required for error handling
import os
from cdh_dav_python.cdc_admin_service import environment_logging
from cdh_dav_python.cdc_admin_service import environment_tracing

# Import from sibling directory ..\databricks_service
OS_NAME = os.name

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("az_storage_service: windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("az_storage_service: non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))


__all__ = ["az_storage_queue", "az_storage_file"]
