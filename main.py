import os

import pandas
import streamlit as st
from pandas import DataFrame

from dao.models.cable_line import CableLine
from dao.models.employee import Employee
from dao.models.workstation import Workstation
from dao.utils.implemented import cable_line_service, employee_service, workstation_service
from dotenv import load_dotenv

# Page settings
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
    layout='wide'
)
load_dotenv()

# Get data
# ----------------------------------------------------------------------------------------------------------------------
cable_lines: list[CableLine] = cable_line_service.get_all()
employees: list[Employee] = employee_service.get_all()
workstations: list[Workstation] = workstation_service.get_all()

df: DataFrame = pandas.DataFrame([(
    cable_line.id,
    cable_line.socket_number,
    cable_line.port_number_socket,
    cable_line.port_number_patch_panel,
    cable_line.length,
    cable_line.employee.full_name,
    cable_line.employee.department.name,
    cable_line.workstation.name,
    cable_line.workstation.ip_address,
    cable_line.workstation.mac_address
) for cable_line in cable_lines],
    columns=[
        'ID',
        '№ розетки',
        '№ порта розетки',
        '№ порта на патчпанели',
        'Длина',
        'ФИО',
        'Подразделение',
        'Имя АРМ',
        'IP адрес АРМ',
        'MAC адрес  АРМ'
    ])

# Main block
# ----------------------------------------------------------------------------------------------------------------------
st.title('Кабельный журнал')
st.dataframe(
    df,
    use_container_width=True,
    column_config={
        '№ розетки': st.column_config.NumberColumn(
            format="%d",
        ),
        '№ порта розетки': st.column_config.NumberColumn(
            format="%d",
        ),
        '№ порта на патчпанели': st.column_config.NumberColumn(
            format="%d",
        ),
        'Длина': st.column_config.NumberColumn(
            format="%d",
        ),
    },
    hide_index=True,
)

# Admin block
# ------------------------------------------------------------------------------
st.divider()
st.title('Панель администратора')

with st.expander('Управление кабелями'):
    create, update, delete = st.columns(3)

    # Create table
    # --------------------------------------------------------------------------
    with create:
        st.header('Добавить')

        with st.form(key='add_form'):
            create_socket_number: int = st.number_input(
                '№ розетки',
                key='create_socket_number',
                value=1,
                min_value=1,
                format='%d',
            )
            create_port_number_socket: int = st.number_input(
                '№ порта розетки',
                key='create_port_number_socket',
                value=1,
                min_value=1,
                format='%d',
            )
            create_port_number_patch_panel: int = st.number_input(
                '№ порта на патчпанели',
                key='create_port_number_patch_panel',
                value=1,
                min_value=1,
                format='%d',
            )
            create_length: int = st.number_input(
                'Длина',
                key='create_length',
                value=1,
                min_value=1,
                format='%d',
            )
            create_employee = st.selectbox(
                'ФИО',
                options=[employee.full_name for employee in employees],
                key='create_employee',
            )
            create_workstation = st.selectbox(
                'Имя АРМ',
                options=[workstation.name for workstation in workstations],
                key='create_workstation'
            )
            admin_password: str = st.text_input(
                'Пароль администратора',
                key='password',
                type='password'
            )

            create_submit_button: bool = st.form_submit_button(
                label='Добавить линию'
            )

            if create_submit_button:
                if not admin_password or admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    data: dict = {
                        'socket_number': st.session_state.create_socket_number,
                        'port_number_socket': st.session_state.create_port_number_socket,
                        'port_number_patch_panel': st.session_state.create_port_number_patch_panel,
                        'length': st.session_state.create_length,
                        'employee_id': [
                            employee.id for employee in employees
                            if employee.full_name == st.session_state.create_employee
                        ][0],
                        'workstation_id': [
                            workstation.id for workstation in workstations
                            if workstation.name == st.session_state.create_workstation
                        ][0],
                    }

                    try:
                        cable_line_service.create(data)

                        st.success(
                            'Линия добавлена',
                            icon='✅'
                        )
                    except RuntimeError:
                        st.error('Ошибка записи', icon='🚨')

    # Update table
    # --------------------------------------------------------------------------
    with update:
        st.header('Обновить')

        # select_department: list[Department] = st.selectbox(
        #     'Выберите подразделение',
        #     options=[department.name for department in departments],
        #     key='select_department',
        # )

        with st.form(key='edit_form'):
            update_cable_line_id: int = st.number_input(
                'ID линии',
                key='update_cable_line_id',
                value=1,
                min_value=1,
                format='%d',
            )
            update_socket_number: int = st.number_input(
                '№ розетки',
                key='update_socket_number',
                value=1,
                min_value=1,
                format='%d',
            )
            update_port_number_socket: int = st.number_input(
                '№ порта розетки',
                key='update_port_number_socket',
                value=1,
                min_value=1,
                format='%d',
            )
            update_port_number_patch_panel: int = st.number_input(
                '№ порта на патчпанели',
                key='update_port_number_patch_panel',
                value=1,
                min_value=1,
                format='%d',
            )
            update_length: int = st.number_input(
                'Длина',
                key='update_length',
                value=1,
                min_value=1,
                format='%d',
            )
            update_employee = st.selectbox(
                'ФИО',
                options=[employee.full_name for employee in employees],
                key='update_employee',
            )
            update_workstation = st.selectbox(
                'Имя АРМ',
                options=[workstation.name for workstation in workstations],
                key='update_workstation'
            )
            update_admin_password: str = st.text_input(
                'Пароль администратора',
                key='update_admin_password',
                type='password'
            )

            update_submit_button: bool = st.form_submit_button(
                label='Обновить линию'
            )

            if update_submit_button:
                if not update_admin_password or update_admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    old_data: dict = {
                        'id': st.session_state.update_cable_line_id,
                    }
                    update_data: dict = {
                        'socket_number': st.session_state.update_socket_number,
                        'port_number_socket': st.session_state.update_port_number_socket,
                        'port_number_patch_panel': st.session_state.update_port_number_patch_panel,
                        'length': st.session_state.update_length,
                        'employee_id': [
                            employee.id for employee in employees
                            if employee.full_name == st.session_state.update_employee
                        ][0],
                        'workstation_id': [
                            workstation.id for workstation in workstations
                            if workstation.name == st.session_state.update_workstation
                        ][0],
                    }

                    try:
                        cable_line_service.update(old_data, update_data)

                        st.success(
                            'Данные линии обновлены',
                            icon='✅'
                        )
                    except RuntimeError:
                        st.error('Ошибка обновления', icon='🚨')

    # Delete table
    # --------------------------------------------------------------------------
    with delete:
        st.header('Удалить')

        with st.form(key='delete_form'):
            uid: int = st.number_input(
                'ID линии',
                key='uid',
                min_value=1
            )
            delete_admin_password: str = st.text_input(
                'Пароль администратора',
                key='delete_password',
                type='password'
            )

            delete_submit_button: bool = st.form_submit_button(
                label='Удалить линию'
            )

            if delete_submit_button:
                if not delete_admin_password or delete_admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    cable_line_service.delete(st.session_state.uid)

                    st.success(
                        'Линия удалена',
                        icon='✅'
                    )
