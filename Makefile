OBS_PROJECT := EA4
zendguard56-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
zendguard55-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
zendguard54-obs : DISABLE_BUILD += repository=CentOS_8 repository=CentOS_9
OBS_PACKAGE := scl-zendguard
include $(EATOOLS_BUILD_DIR)obs-scl.mk