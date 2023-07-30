import os

import pandas
import streamlit as st
from pandas import DataFrame

from dao.models.workstation import Workstation
from dao.utils.implemented import workstation_service
from dotenv import load_dotenv

# Page settings
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
    layout='wide'
)
load_dotenv()

# Get data
# ----------------------------------------------------------------------------------------------------------------------
workstations: list[Workstation] = workstation_service.get_all()

df: DataFrame = pandas.DataFrame([(
    workstation.id,
    workstation.name,
    workstation.ip_address,
    workstation.mac_address,
) for workstation in workstations],
    columns=[
        'ID',
        'Имя',
        'IP адрес',
        'MAC адрес',
    ])

# Main block
# ----------------------------------------------------------------------------------------------------------------------
st.title('Список автоматизированных рабочих мест')
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# Admin block
# ------------------------------------------------------------------------------
st.divider()
st.title('Панель администратора')

with st.expander('Управление АРМ'):
    create, update, delete = st.columns(3)

    # Create table
    # --------------------------------------------------------------------------
    with create:
        st.header('Добавить')

        with st.form(key='add_form'):
            workstation_name: str = st.text_input(
                'Имя АРМ',
                key='workstation_name'
            )
            ip_address: str = st.text_input(
                'IP адрес',
                key='ip_address'
            )
            mac_address: str = st.text_input(
                'MAC адрес',
                key='mac_address'
            )
            admin_password: str = st.text_input(
                'Пароль администратора',
                key='password',
                type='password'
            )

            create_submit_button = st.form_submit_button(
                label='Добавить АРМ'
            )

            if create_submit_button:
                if not admin_password or admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    data: dict = {
                        'name': st.session_state.workstation_name,
                        'ip_address': st.session_state.ip_address,
                        'mac_address': st.session_state.mac_address,
                    }

                    try:
                        workstation_service.create(data)

                        st.success(
                            'АРМ успешно добавлена',
                            icon='✅'
                        )
                    except RuntimeError:
                        st.error('Ошибка записи', icon='🚨')

    # Update table
    # --------------------------------------------------------------------------
    with update:
        st.header('Обновить')

        select_workstation: list[Workstation] = st.selectbox(
            'Выберите АРМ',
            options=[workstation.name for workstation in workstations],
            key='select_workstation',
        )

        with st.form(key='edit_form'):
            edit_workstation_name: str = st.text_input(
                'Имя АРМ',
                key='edit_workstation_name',
                value=st.session_state.select_workstation
            )
            edit_ip_address: str = st.text_input(
                'IP адрес',
                key='edit_ip_address'
            )
            edit_mac_address: str = st.text_input(
                'MAC адрес',
                key='edit_mac_address'
            )
            edit_admin_password: str = st.text_input(
                'Пароль администратора',
                key='edit_admin_password',
                type='password'
            )

            update_submit_button = st.form_submit_button(
                label='Обновить данные АРМ'
            )

            if update_submit_button:
                if not edit_admin_password or edit_admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    old_data: dict = {
                        'name': st.session_state.select_workstation
                    }
                    update_data: dict = {
                        'name': st.session_state.edit_workstation_name,
                        'ip_address': st.session_state.edit_ip_address,
                        'mac_address': st.session_state.edit_mac_address,
                    }
                    try:
                        workstation_service.update(old_data, update_data)

                        st.success(
                            'Данные АРМ обновлены',
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
                'ID АРМ',
                key='uid',
                min_value=1
            )
            delete_admin_password: str = st.text_input(
                'Пароль администратора',
                key='delete_password',
                type='password'
            )

            delete_submit_button: bool = st.form_submit_button(
                label='Удалить АРМ'
            )

            if delete_submit_button:
                if not delete_admin_password or delete_admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    workstation_service.delete(st.session_state.uid)

                    st.success(
                        'АРМ удалена',
                        icon='✅'
                    )
