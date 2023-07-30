from dao.cable_line_dao import CableLineDAO
from dao.department_dao import DepartmentDAO
from dao.employee_dao import EmployeeDAO
from dao.server_room_dao import ServerRoomDAO
from dao.workstation_dao import WorkstationDAO
from database.initialize_engine import DatabaseSession, db_engine
from services.cable_line_service import CableLineService
from services.department_service import DepartmentService
from services.employee_service import EmployeeService
from services.server_room_service import ServerRoomService
from services.workstation_service import WorkstationService

# Create session
# ----------------------------------------------------------------------------------------------------------------------
session = DatabaseSession(db_engine).create_session()

# Create DAO
# ----------------------------------------------------------------------------------------------------------------------
employee_dao = EmployeeDAO(session)
cable_line_dao = CableLineDAO(session)
department_dao = DepartmentDAO(session)
server_room_dao = ServerRoomDAO(session)
workstation_dao = WorkstationDAO(session)

# Create service
# ----------------------------------------------------------------------------------------------------------------------
employee_service = EmployeeService(employee_dao)
cable_line_service = CableLineService(cable_line_dao)
department_service = DepartmentService(department_dao)
server_room_service = ServerRoomService(server_room_dao)
workstation_service = WorkstationService(workstation_dao)
