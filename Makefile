# Makefile for source rpm: coreutils
# $Id$
NAME := coreutils
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
