/* Copyright 2019 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/


#include <limits>
#include "tensorflow/lite/c/common.h"
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/kernels/internal/tensor_ctypes.h"
#include "model_settings.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
//#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "bkgmodel_tflite.h"
#include "tensorflow/lite/micro/testing/micro_test.h"
#include "tensorflow/lite/schema/schema_generated.h"
#include "bkgpng.h"

// Globals, used for compatibility with Arduino-style sketches.
namespace micro_test {            
  int tests_passed;                 
  int tests_failed;                 
  bool is_test_complete;            
  bool did_test_fail;               
 }   


namespace {
tflite::ErrorReporter* error_reporter = nullptr;
const tflite::Model* model = nullptr;
tflite::MicroInterpreter* interpreter = nullptr;
TfLiteTensor* input = nullptr;

// In order to use optimized tensorflow lite kernels, a signed int8_t quantized
// model is preferred over the legacy unsigned model format. This means that
// throughout this project, input images must be converted from unisgned to
// signed format. The easiest and quickest way to convert from unsigned to
// signed 8-bit integers is to subtract 128 from the unsigned value to get a
// signed value.

// An area of memory to use for input, output, and intermediate arrays.
// BKGconstexpr int kTensorArenaSize = 136 * 1024;
constexpr int kTensorArenaSize = 2 * 1024 * 1024;
static uint8_t tensor_arena[kTensorArenaSize];
}  // namespace

// The name of this function is important for Arduino compatibility.
void setup() {
  tflite::InitializeTarget();

  // Set up logging. Google style is to avoid globals or statics because of
  // lifetime uncertainty, but since this has a trivial destructor it's okay.
  // NOLINTNEXTLINE(runtime-global-variables)
  static tflite::MicroErrorReporter micro_error_reporter;
  error_reporter = &micro_error_reporter;

  // Map the model into a usable data structure. This doesn't involve any
  // copying or parsing, it's a very lightweight operation.
  model = tflite::GetModel(bkgmodel_tflite);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    TF_LITE_REPORT_ERROR(error_reporter,
                         "Model provided is schema version %d not equal "
                         "to supported version %d.",
                         model->version(), TFLITE_SCHEMA_VERSION);
    return;
  }

  // Pull in only the operation implementations we need.
  // This relies on a complete list of all the ops needed by this graph.
  // An easier approach is to just use the AllOpsResolver, but this will
  // incur some penalty in code space for op implementations that are not
  // needed by this graph.
  //
  // tflite::AllOpsResolver resolver;
  // NOLINTNEXTLINE(runtime-global-variables)


/*
  static tflite::MicroMutableOpResolver<5> micro_op_resolver;
  micro_op_resolver.AddAveragePool2D();
  micro_op_resolver.AddConv2D();
  micro_op_resolver.AddDepthwiseConv2D();
  micro_op_resolver.AddReshape();
  micro_op_resolver.AddSoftmax();
*/
  static tflite::AllOpsResolver micro_op_resolver;

  // Build an interpreter to run the model with.
  // NOLINTNEXTLINE(runtime-global-variables)
  static tflite::MicroInterpreter static_interpreter(
      model, micro_op_resolver, tensor_arena, kTensorArenaSize, error_reporter);
  interpreter = &static_interpreter;

  // Allocate memory from the tensor_arena for the model's tensors.
  TfLiteStatus allocate_status = interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    TF_LITE_REPORT_ERROR(error_reporter, "AllocateTensors() failed");
    return;
  }

  // Get information about the memory area to use for the model's input.
  input = interpreter->input(0);
}


// The name of this function is important for Arduino compatibility.
void infer(char *filename) {
	int i;
	/*
  // Get image from provider.
  if (kTfLiteOk != GetImage(error_reporter, kNumCols, kNumRows, kNumChannels,
                            input->data.int8)) {
    TF_LITE_REPORT_ERROR(error_reporter, "Image capture failed.");
  }

	memcpy(input->data.int8,g_five_gray_image_data,g_five_gray_image_data_size);
	*/
	printf("Reading %s\n",filename);
	read_png_file(filename, input->data.int8, kNumCols+kNumRows * kNumChannels);
  // Run the model on this input and make sure it succeeds.
  if (kTfLiteOk != interpreter->Invoke()) {
    TF_LITE_REPORT_ERROR(error_reporter, "Invoke failed.");
  }

  TfLiteTensor* output = interpreter->output(0);

	printf("Input Tensor:\n");
	printf("  Dims Size %d Type %d\n",input->dims->size,input->type);
	for (i=0;i<input->dims->size;i++)
		printf(" %d ",input->dims->data[i]);
	printf("\n");

	printf("\nOutput Tensor:\n");
	printf("  Dims Size %d Type %d\n",output->dims->size,output->type);
	for (i=0;i<output->dims->size;i++)
		printf(" %d ",output->dims->data[i]);
	printf("\n");
  // Get the output from the model, and make sure it's the expected size and
  // type. THIS MAY ALL BE WRONG??
  TF_LITE_MICRO_EXPECT_EQ(2, output->dims->size);
  TF_LITE_MICRO_EXPECT_EQ(1, output->dims->data[0]);
  TF_LITE_MICRO_EXPECT_EQ(kCategoryCount, output->dims->data[1]);
  TF_LITE_MICRO_EXPECT_EQ(kTfLiteInt8, input->type);
  TF_LITE_MICRO_EXPECT_EQ(kTfLiteInt8, output->type);
  //TF_LITE_MICRO_EXPECT_EQ(kTfLiteFloat32, output->type);

  // Process the inference results.
	// ["five", "horns", "peace", "sideeye", "three", "thumbs_up"]
  //int8_t person_score = output->data.uint8[kPersonIndex];
  //int8_t no_person_score = output->data.uint8[kNotAPersonIndex];
	//printf("Person Score %d no_person_score %d\n",person_score,no_person_score);
	printf("Category count is %d\n",kCategoryCount);
	for (i=0;i<kCategoryCount;i++) {
			printf("%s",kCategoryLabels[i]);
			//printf("%s %0.4f",kCategoryLabels[i], double(tflite::GetTensorData<float>(output)[i]));
			/* printf(" %4.4f ",double(tflite::GetTensorData<double>(output)[i])); */
			printf(" %4d\n",tflite::GetTensorData<int8_t>(output)[i]);
	}
/*
	printf("Five %d\n",int8_t(output->data.uint8[0]));
	printf("Horns %d\n",int8_t(output->data.uint8[1]));
	printf("Peace %d\n",int8_t(output->data.uint8[2]));
	printf("Sideeye %d\n",int8_t(output->data.uint8[3]));
	printf("three %d\n",int8_t(output->data.uint8[4]));
	printf("Thumbs_up %d\n",int8_t(output->data.uint8[5]));
*/
  //RespondToDetection(error_reporter, person_score, no_person_score);
}

int main(int argc, char* argv[]) {
	int i;
	printf("SETUP\n");
  setup();
	printf("LOOP\n");
	for (i=1;i<argc;i++)
  infer(argv[i]);
}
