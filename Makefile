OBS_PROJECT := EA4
zendguard56-obs : DISABLE_BUILD += repository=CentOS_8
zendguard55-obs : DISABLE_BUILD += repository=CentOS_8
zendguard54-obs : DISABLE_BUILD += repository=CentOS_8
OBS_PACKAGE := scl-zendguard
include $(EATOOLS_BUILD_DIR)obs-scl.mk