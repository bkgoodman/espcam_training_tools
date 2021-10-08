/*
 * Copyright 2002-2010 Guillaume Cottenceau.
 *
 * This software may be freely redistributed under the terms
 * of the X11 license.
 *
 */

#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdarg.h>

#define PNG_DEBUG 3
#include <png.h>

void abort_(const char * s, ...)
{
        va_list args;
        va_start(args, s);
        vfprintf(stderr, s, args);
        fprintf(stderr, "\n");
        va_end(args);
        exit(0);	
				// abort();
}


void read_png_file(char* file_name, void *memptr, size_t bufsz)
{
				int y;

				int width, height;
				png_byte color_type;
				png_byte bit_depth;
				size_t rowbytes;

				png_structp png_ptr;
				png_infop info_ptr;
        char header[8];    // 8 is the maximum size that can be checked

        /* open file and test for it being a png */
        FILE *fp = fopen(file_name, "rb");
        if (!fp)
                abort_("[read_png_file] File %s could not be opened for reading", file_name);
        if (fread(header, 1, 8, fp) != 8)
					abort_("PNG read header failed");
        if (png_sig_cmp((png_const_bytep) header, 0, 8))
                abort_("[read_png_file] File %s is not recognized as a PNG file", file_name);


        /* initialize stuff */
        png_ptr = png_create_read_struct(PNG_LIBPNG_VER_STRING, NULL, NULL, NULL);

        if (!png_ptr)
                abort_("[read_png_file] png_create_read_struct failed");

        info_ptr = png_create_info_struct(png_ptr);
        if (!info_ptr)
                abort_("[read_png_file] png_create_info_struct failed");

        if (setjmp(png_jmpbuf(png_ptr)))
                abort_("[read_png_file] Error during init_io");

        png_init_io(png_ptr, fp);
        png_set_sig_bytes(png_ptr, 8);

        png_read_info(png_ptr, info_ptr);

        width = png_get_image_width(png_ptr, info_ptr);
        height = png_get_image_height(png_ptr, info_ptr);
        color_type = png_get_color_type(png_ptr, info_ptr);
        bit_depth = png_get_bit_depth(png_ptr, info_ptr);
				rowbytes = png_get_rowbytes(png_ptr,info_ptr);

				printf("READ_PNG %s: Width %d height %d color_type %d bitdepth %d rowbytes %ld\n",file_name,width,height,color_type,bit_depth, rowbytes);
        png_set_interlace_handling(png_ptr);
        png_read_update_info(png_ptr, info_ptr);


        /* read file */
        if (setjmp(png_jmpbuf(png_ptr)))
                abort_("[read_png_file] Error during read_image");

        for (y=0; y<height; y++) {
                //row_pointers[y] = (png_byte*) malloc(png_get_rowbytes(png_ptr,info_ptr));
                png_bytep row_pointer = (png_byte*) memptr+(y*rowbytes);
                //printf ("Row %d Buffer at %p\n",y,row_pointer);
								if (memptr) png_read_row(png_ptr, row_pointer, NULL);
				}


        fclose(fp);

}



#ifdef PNG_APP
int main(int argc, char **argv)
{
        if (argc != 2)
                abort_("Usage: program_name <file_in>");

        read_png_file(argv[1],0L,0);

        return 0;
}
#endif
