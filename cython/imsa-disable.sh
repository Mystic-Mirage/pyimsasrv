#!/bin/bash

LANG=en wine net stop imsaservice
wine regedit imsa-disable.reg

