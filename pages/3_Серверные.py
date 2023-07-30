import os

import pandas
import streamlit as st
from pandas import DataFrame
from sqlalchemy.exc import IntegrityError, PendingRollbackError

from dao.models.server_room import ServerRoom
from dao.utils.implemented import server_room_service, session
from dotenv import load_dotenv

# Page settings
# ----------------------------------------------------------------------------------------------------------------------
st.set_page_config(
    layout='wide'
)
load_dotenv()

# Get data
# ----------------------------------------------------------------------------------------------------------------------
server_rooms: list[ServerRoom] = server_room_service.get_all()

df: DataFrame = pandas.DataFrame([(
    server_room.id,
    server_room.number,
) for server_room in server_rooms],
    columns=[
        'ID',
        'Номер серверной'
    ])

# Main block
# ----------------------------------------------------------------------------------------------------------------------
st.title('Список серверных')
st.dataframe(df,
             use_container_width=True,
             hide_index=True
             )

# Admin block
# ------------------------------------------------------------------------------
st.divider()
st.title('Панель администратора')

with st.expander('Управление серверными'):
    create, update, delete = st.columns(3)

    # Create table
    # --------------------------------------------------------------------------
    with create:
        st.header('Добавить')

        with st.form(key='add_form'):
            number: int = st.number_input(
                'Номер серверной',
                key='number',
                value=1,
                min_value=1,
            )
            admin_password: str = st.text_input(
                'Пароль администратора',
                key='password',
                type='password'
            )

            create_submit_button: bool = st.form_submit_button(
                label='Добавить серверную'
            )

            if create_submit_button:
                if not admin_password or admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    data: dict = {
                        'number': st.session_state.number,
                    }

                    try:
                        server_room_service.create(data)

                        st.success(
                            'Серверная добавлена',
                            icon='✅'
                        )
                    except RuntimeError:
                        st.error('Ошибка записи', icon='🚨')

    # Update table
    # --------------------------------------------------------------------------
    with update:
        st.header('Обновить')

        select_server_room: list[ServerRoom] = st.selectbox(
            'Выберите серверную',
            options=[server_room.number for server_room in server_rooms],
            key='select_server_room',
        )

        with st.form(key='edit_form'):
            edit_server_room_number: int = st.number_input(
                'Номер серверной',
                key='edit_server_room_number',
                value=st.session_state.select_server_room if st.session_state.select_server_room else 1,
                min_value=1
            )

            edit_admin_password: str = st.text_input(
                'Пароль администратора',
                key='edit_admin_password',
                type='password'
            )

            update_submit_button: bool = st.form_submit_button(
                label='Обновить серверную'
            )

            if update_submit_button:
                if not edit_admin_password or edit_admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    old_data: dict = {
                        'number': st.session_state.select_server_room,
                    }
                    update_data: dict = {
                        'number': st.session_state.edit_server_room_number,
                    }
                    try:
                        server_room_service.update(old_data, update_data)

                        st.success(
                            'Данные серверной обновлены',
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
                'ID серверной',
                key='uid',
                min_value=1
            )
            delete_admin_password: str = st.text_input(
                'Пароль администратора',
                key='delete_password',
                type='password'
            )

            delete_submit_button: bool = st.form_submit_button(
                label='Удалить серверную'
            )

            if delete_submit_button:
                if not delete_admin_password or delete_admin_password != os.environ.get('ADMIN_PASSWORD'):
                    st.warning(
                        'Введен неверный пароль',
                        icon='⚠️'
                    )
                else:
                    server_room_service.delete(st.session_state.uid)
                    st.success(
                        'Серверная удалена',
                        icon='✅'
                    )
