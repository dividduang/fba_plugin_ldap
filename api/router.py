#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import APIRouter

from backend.core.conf import settings
from backend.plugin.ldap_auth.api.v1.ldap_auth import router as ldap_auth_router

v1 = APIRouter(prefix=f'{settings.FASTAPI_API_V1_PATH}/ldap_auth')

v1.include_router(ldap_auth_router, tags=['LDAP'])

