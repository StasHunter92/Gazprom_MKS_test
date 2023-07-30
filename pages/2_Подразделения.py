import os

import pandas
import streamlit as st
from pandas import DataFrame

from dao.models.department import Department
from dao.utils.implemented import department_service
from dotenv import load_dotenv

# Page settings
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
    layout='wide'
)
load_dotenv()

# Get data
# ----------------------------------------------------------------------------------------------------------------------
departments: list[Department] = department_service.get_all()

df: DataFrame = pandas.DataFrame([(
    department.id,
    department.name,
) for department in departments],
    columns=[
        'ID',
        'Подразделение'
    ])

# Main block
# ----------------------------------------------------------------------------------------------------------------------
st.title('Список подразделений')
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)

# Admin block
# ------------------------------------------------------------------------------
st.divider()
st.title('Панель администратора')

with st.expander('Управление подразделениями'):
    create, update, delete = st.columns(3)

    # Create table
    # --------------------------------------------------------------------------
    with create:
        st.header('Добавить')

        with st.form(key='add_form'):
            department_name: str = st.text_input(
                'Название подразделения',
                key='department_name'
            )
            admin_password: str = st.text_input(
                'Пароль администратора',
                key='password',
                type='password'
            )

            create_submit_button: bool = st.form_submit_button(
                label='Добавить подразделение'
            )

            if create_submit_button:
                if not admin_password or admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    data: dict = {
                        'name': st.session_state.department_name,
                    }

                    try:
                        department_service.create(data)

                        st.success(
                            'Подразделение добавлено',
                            icon='✅'
                        )
                    except RuntimeError:
                        st.error('Ошибка записи', icon='🚨')

    # Update table
    # --------------------------------------------------------------------------
    with update:
        st.header('Обновить')

        select_department: list[Department] = st.selectbox(
            'Выберите подразделение',
            options=[department.name for department in departments],
            key='select_department',
        )

        with st.form(key='edit_form'):
            edit_department_name: str = st.text_input(
                'Название подразделения',
                key='edit_department_name',
                value=st.session_state.select_department
            )

            edit_admin_password: str = st.text_input(
                'Пароль администратора',
                key='edit_admin_password',
                type='password'
            )

            update_submit_button: bool = st.form_submit_button(
                label='Обновить подразделение'
            )

            if update_submit_button:
                if not edit_admin_password or edit_admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    old_data: dict = {
                        'name': st.session_state.select_department,
                    }
                    update_data: dict = {
                        'name': st.session_state.edit_department_name,
                    }

                    try:
                        department_service.update(old_data, update_data)

                        st.success(
                            'Данные подразделения обновлены',
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
                'ID подразделения',
                key='uid',
                min_value=1
            )
            delete_admin_password: str = st.text_input(
                'Пароль администратора',
                key='delete_password',
                type='password'
            )

            delete_submit_button: bool = st.form_submit_button(
                label='Удалить подразделение'
            )

            if delete_submit_button:
                if not delete_admin_password or delete_admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    department_service.delete(st.session_state.uid)

                    st.success(
                        'Подразделение удалено',
                        icon='✅'
                    )
