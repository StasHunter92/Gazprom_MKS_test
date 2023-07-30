import os

import pandas
import streamlit as st
from pandas import DataFrame

from dao.models.department import Department
from dao.models.employee import Employee
from dao.utils.implemented import employee_service, department_service
from dotenv import load_dotenv

# Page settings
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
    layout='wide'
)
load_dotenv()

# Get data
# ----------------------------------------------------------------------------------------------------------------------
employees: list[Employee] = employee_service.get_all()
departments: list[Department] = department_service.get_all()

df: DataFrame = pandas.DataFrame([(
    employee.id,
    employee.last_name,
    employee.first_name,
    employee.patronymic,
    employee.department.name if employee.department is not None else ''
) for employee in employees],
    columns=[
        'ID',
        'Фамилия',
        'Имя',
        'Отчество',
        'Отдел'
    ])

# Main block
# ----------------------------------------------------------------------------------------------------------------------
st.title('Список сотрудников')
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)

# Admin block
# ------------------------------------------------------------------------------
st.divider()
st.title('Панель администратора')

with st.expander('Управление сотрудниками'):
    create, update, delete = st.columns(3)

    # Create table
    # --------------------------------------------------------------------------
    with create:
        st.header('Добавить')

        with st.form(key='add_form'):
            last_name: str = st.text_input(
                'Фамилия',
                key='last_name'
            )
            first_name: str = st.text_input(
                'Имя',
                key='first_name'
            )
            patronymic: str = st.text_input(
                'Отчество',
                key='patronymic'
            )
            department = st.selectbox(
                'Подразделение',
                options=[department.name for department in departments],
                key='department'
            )
            admin_password: str = st.text_input(
                'Пароль администратора',
                key='password',
                type='password'
            )

            create_submit_button: bool = st.form_submit_button(
                label='Добавить сотрудника'
            )

            if create_submit_button:
                if not admin_password or admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    data: dict = {
                        'first_name': st.session_state.first_name,
                        'last_name': st.session_state.last_name,
                        'patronymic': st.session_state.patronymic,
                        'department_id': [
                            department.id for department in departments
                            if department.name == st.session_state.department
                        ][0]
                    }

                    try:
                        employee_service.create(data)

                        st.success(
                            'Сотрудник добавлен',
                            icon='✅'
                        )
                    except RuntimeError:
                        st.error('Ошибка записи', icon='🚨')

    # Update table
    # --------------------------------------------------------------------------
    with update:
        st.header('Обновить')

        select_employee: list[Employee] = st.selectbox(
            'Выберите сотрудника',
            options=[employee.full_name for employee in employees],
            key='select_employee',
        )

        with st.form(key='edit_form'):
            edit_last_name: str = st.text_input(
                'Фамилия',
                key='edit_last_name',
                value=st.session_state.select_employee.split()[0] if st.session_state.select_employee else None
            )
            edit_first_name: str = st.text_input(
                'Имя',
                key='edit_first_name',
                value=st.session_state.select_employee.split()[1] if st.session_state.select_employee else None
            )
            edit_patronymic: str = st.text_input(
                'Отчество',
                key='edit_patronymic',
                value=st.session_state.select_employee.split()[2] if st.session_state.select_employee else None
            )
            edit_department = st.selectbox(
                'Подразделение',
                options=[department.name for department in departments],
                key='edit_department'
            )
            edit_admin_password: str = st.text_input(
                'Пароль администратора',
                key='edit_admin_password',
                type='password'
            )

            update_submit_button: bool = st.form_submit_button(
                label='Обновить сотрудника'
            )

            if update_submit_button:
                if not edit_admin_password or edit_admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    old_data: dict = {
                        'first_name': st.session_state.select_employee.split()[1],
                        'last_name': st.session_state.select_employee.split()[0],
                        'patronymic': st.session_state.select_employee.split()[2],
                    }
                    update_data: dict = {
                        'first_name': st.session_state.edit_first_name,
                        'last_name': st.session_state.edit_last_name,
                        'patronymic': st.session_state.edit_patronymic,
                        'department_id': [
                            department.id for department in departments
                            if department.name == st.session_state.edit_department
                        ][0]
                    }

                    try:
                        employee_service.update(old_data, update_data)

                        st.success(
                            'Сотрудник обновлен',
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
                'ID сотрудника',
                key='uid',
                min_value=1
            )
            delete_admin_password: str = st.text_input(
                'Пароль администратора',
                key='delete_password',
                type='password'
            )

            delete_submit_button: bool = st.form_submit_button(
                label='Удалить сотрудника',
            )

            if delete_submit_button:
                if not delete_admin_password or delete_admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )

                else:
                    employee_service.delete(st.session_state.uid)

                    st.success(
                        'Сотрудник удален',
                        icon='✅'
                    )
