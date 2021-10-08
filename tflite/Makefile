#!/bin/sh

# https://www.tensorflow.org/lite/guide/inference

CC=g++
TFROOT=/home/bkg/tflite-micro
CC_FLAGS=-std=c++11 -fno-rtti -fno-exceptions -fno-threadsafe-statics -Werror -fno-unwind-tables -ffunction-sections -fdata-sections -fmessage-length=0 -DTF_LITE_STATIC_MEMORY -DTF_LITE_DISABLE_X86_NEON -Wsign-compare -Wdouble-promotion -Wshadow -Wunused-variable -Wmissing-field-initializers -Wunused-function -Wswitch -Wvla -Wall -Wextra -Wstrict-aliasing -Wno-unused-parameter  -DTF_LITE_USE_CTIME -Os -I. -I${TFROOT} -I${TFROOT}/tensorflow/lite/micro/tools/make/downloads/gemmlowp -I${TFROOT}/tensorflow/lite/micro/tools/make/downloads/flatbuffers/include -I${TFROOT}/tensorflow/lite/micro/tools/make/downloads/ruy -I${TFROOT}/tensorflow/lite/micro/tools/make/gen/linux_x86_64_default/genfiles/ -I${TFROOT}/tensorflow/lite/micro/tools/make/downloads/kissfft

TOOLS=${TFROOT}/tensorflow/lite/micro/tools
OBJ_DIR=obj
GEN=gen
OBJCOREGENFILE=genfile
TF_LIB_DIR=${TFROOT}/tensorflow/lite/micro/tools/make/gen/linux_x86_64_default/lib/
SRCDIR=.
IMAGES=$(shell ls images)

SOURCES=bkgtest.cc model_settings.cc png.cc

all: bkgtflite

test: bkgtflite $(IMAGES:%.jpg=${GEN}/%_grey.png)
	$(foreach f,$^,$^)

bkgtflite: $(SOURCES:%.cc=${OBJ_DIR}/%.o) 
	${CC} ${CC_FLAGS}  -o $@ $^ ${TF_LIB_DIR}/libtensorflow-microlite.a -Wl,--fatal-warnings -Wl,--gc-sections -lm -lpng

.PHONY: clean
clean:
	rm -rf bkgtflite obj/ gen/

obj/%.o: %.cc
	mkdir -p $(@D)
	${CC} ${CC_FLAGS} -c $< -o $@


#$(IMAGES:%.jpg=${OBJ_DIR}/%img.o): %.jpg
#images/%.jpg: ${OBJ_DIR}/%_img.o 
#${OBJ_DIR}/%_img.o: images/%.jpg

${GEN}/%_grey.bmp: images/%.png
	convert $^ -set colorspace Gray -separate -average $@

${GEN}/%_grey.png: images/%.jpg
	mkdir -p $(@D)
	convert $^ -set colorspace Gray -separate -average $@

${GEN}/%.h: ${GEN}/%_grey.bmp
	mkdir -p $(@D)
	python ${TOOLS}/generate_cc_arrays.py $@ $^

${GEN}/%.cc: ${GEN}/%_grey.bmp
	mkdir -p $(@D)
	python ${TOOLS}/generate_cc_arrays.py $@ $^

${OBJ_DIR}/%_img.o: ${GEN}/%.cc
	mkdir -p $(@D)
	gcc -std=c++11 -fno-rtti -fno-exceptions -fno-threadsafe-statics -fno-unwind-tables -ffunction-sections -fdata-sections -fmessage-length=0  -I. -c $< -o $@

.SECONDARY: ${IMAGES:%.jpg=${GEN}/%.cc} ${IMAGES:%.jpg=${GEN}/%_img.cc} ${IMAGES:%.jpg=${GEN}/%_img.h} ${IMAGES:%.jpg=${GEN}/%_grey.bmp} 

# convert five.jpg -set colorspace Gray -separate -average five_gray.bmp
# generate_cc_arrays output input
#for img in five horns confused peace ; do
#	convert ${IMAGES}/${img}.jpg -set colorspace Gray -separate -average ${GEN}/${img}_gray.bmp
#	python ${TOOLS}/generate_cc_arrays.py ${GEN}/${img}.cc ${GEN}/${img}_gray.bmp
#	python ${TOOLS}/generate_cc_arrays.py ${GEN}/${img}.h ${GEN}/${img}_gray.bmp
#	${CC} ${GCC_FLAGS} ${GEN}/${img}.cc -o ${OBJ_DIR}/${img}.o
#done

#${CC} ${GCC_FLAGS} ${SRCDIR}/bkgtest.cc -o ${OBJ_DIR}/bkgtflite.o
#${CC} ${GCC_FLAGS} ${SRCDIR}/model_settings.cc -o ${OBJ_DIR}/model_settings.o

#${CC} ${GCC_FLAGS} ${SRCDIR}/image_provider.cc -o ${OBJ_DIR}/image_provider.o



