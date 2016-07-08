#include <vector>
#include <map>
#include <algorithm>

#include <stdexcept>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sstream>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <assert.h>
#include <time.h>
#include <omp.h>

#include "imagehelper.h"
#include "helper.h"
#include <Magick++.h>

#define CHUNK 200

using namespace std;
using namespace Magick;

// set these environment variables to non-empty string to enable them
const int no_singleton = (getenv("WITH_SINGLETON")==NULL);

void help_and_exit() {
	cerr << "usage: cor_img <win size> <step size> <sd thres> <cor thres> <value thres> <label> <input dir> <output dir> " << endl;
    cerr << endl;
    exit(0);
}

int main(int argc, char* argv[]) {

    InitializeMagick(*argv);

    char** arg_end = argv+argc;
    char** arg_next = argv+1;

    if (arg_next>=arg_end) help_and_exit();
    const int w_size = parse_int(*arg_next++);
    if (w_size<2) {
        cerr << "window size " << w_size << " < 2" << endl;
        exit(255);
    }

    const int w_inc = parse_int(*arg_next++);
    if (w_size<1) {
        cerr << "window increment " << w_inc << " < 1" << endl;
        exit(255);
    }
    if (w_size % w_inc!=0) {
        cerr << "window size " << w_size << " is not a multiple of " << w_inc << endl;
        exit(255);
    }

    if (arg_next>=arg_end) help_and_exit();
    const double sd_thres = parse_double(*arg_next++);
    if (arg_next>=arg_end) help_and_exit();
    const double cor_thres = parse_double(*arg_next++);
    if (cor_thres>=1) {
        cerr << "cor thres " << cor_thres << " is too high" << endl;
        exit(255);
    }
	if (arg_next>=arg_end) help_and_exit();
    const int pvalue_thres = parse_int(*arg_next++);
	if (arg_next>=arg_end) help_and_exit();
    char* label = *arg_next++;
    if (arg_next>=arg_end) help_and_exit();
    char* input_dir = *arg_next++;
    if (arg_next>=arg_end) help_and_exit();
    string output_dir(*arg_next++);

    vector<string> filenames;
    find_tiff_in_dir(input_dir, filenames);
    sort(filenames.begin(), filenames.end(), image_fname_comparator);

    time_t t0, t1, t00;
    time(&t00);
    t0 = t00;

    Image images[w_size];
    Pixels* views[w_size];
    const PixelPacket* pixels[w_size];
    for (int i=0;i<w_size;i++) {
        views[i] = NULL;
    }

	FILE *fpw;
	char filew[512];
	sprintf(filew,"%s%d.pair","cor_weights_cor", int(cor_thres*100));
	if ((fpw = fopen(filew,"w"))==NULL)
	{
		printf("cannot open file\n");
	}
	

	/************************************************************************/
	/************************************************************************/

 	int npixels=-1; //TODO get number of pixels
	int n=0;
	//for each file
    for (int file_index=0;file_index<filenames.size();file_index++) {
       
        // this make sure the array index in the following line is valid
        if (file_index<w_size-1) continue;

        // make less overlapping sliding windows to speed up the process
        if ((file_index+1)%w_inc!=0) continue;
        
		//int index = file_index-w_size+1;
		int frame_num = atoi(frame_number.c_str()); //TODO get frame number
		
		n++;		       
		
		//TODO THIS IS THE RIGHT MOMENT TO SEE IF WE WANT TO Z-NORMALIZE THE TIME SERIES

        // compute standard deviation
		double s1[npixels], s2[npixels], mean[npixels], sd[npixels];
		double pvalue[npixels];

		// compute correlated nodes
		int nodes[npixels];
		for (int i=0; i<npixels; i++)
			nodes[i] = -1; //TODO is this initialization really needed??
		
		int n = 0, t=0, r=0;
		
//#pragma omp parallel for shared(images,s1,s2,mean,sd) schedule(dynamic,CHUNK)  // not really work paralle ... ?

//shared means that that variable is shared among threads
//private means the opposite
//schedule(static) is that with static, the chunks can be somewhat computed and scheduled to threads during compilation, 
//while with dynamic it is done during run-time 

        for (int i=0;i<npixels;i++) {
            double& x1 = s1[i] = 0;
            double& x2 = s2[i] = 0;
            for (int s=0;s<w_size;s++) {
                const PixelPacket *p=&pixels[s][i];
				const double value = (p->red + p->blue + p->green)/3.0/16;  // 12 bit				
                x1 += value;
                x2 += value*value;
            }
            mean[i] = s1[i]/w_size;
            sd[i] = sqrt((s2[i] - s1[i]*s1[i]/w_size)/(w_size-1));
        }


        // compute correlation coefficient
        static const double npairs = npixels*(npixels-1L)/2;
        static long npairs_done = 0, n_corpairs=0;
		int num_active=0, old_num_active=0, active_number=0;
		int num_edge=0, old_num_edge=0, edge_number=0;
		stringstream stream_node, stream_edge;

        for (int i=0;i<npixels;i++) {
			if (sd[i]<sd_thres) continue;
			int x0 = get_x(i), y0 = get_y(i);

			if (mean[i]>=pvalue_thres) {
//#pragma omp parallel for shared(p, n_corpairs) schedule(dynamic,CHUNK)
#pragma omp parallel for schedule(dynamic,CHUNK)
                for (int j=i+1;j<npixels;j++) {
                    if (sd[j]<sd_thres) continue;
					if (mean[j]<pvalue_thres) continue;
					int x1 = get_x(j), y1 = get_y(j);
                    double sum_xy=0.0;
                    for (int s=0;s<w_size;s++) {
                        const PixelPacket *p1=&pixels[s][i];
                        const PixelPacket *p2=&pixels[s][j];
						const double value1 = (double) (p1->red + p1->blue + p1->green)/3.0/16;  // 12 bit
                        const double value2 = (double) (p2->red + p2->blue + p2->green)/3.0/16;  // 12 bit

                        sum_xy += value1*value2;
                    }
					
                    double cor = (sum_xy - s1[i]*s1[j]/w_size)/(w_size-1)/sd[i]/sd[j]; 

					if (cor>=cor_thres) {
                        int color = cor>0?0x00FF00:0xFF0000;
						fprintf(fpw, "%d	%d	%d	%f\n",frame_num,y0*pic_w+x0,y1*pic_w+x1,cor);

//#pragma omp critical
                        //{
                            n_corpairs++;
                            draw_edge(p, pic_w, pic_h, x0, y0, x1, y1, color);
							num_edge++;

							draw_cross(p, pic_w, pic_h, x0, y0, 0x0000FF);
							draw_cross(p, pic_w, pic_h, x1, y1, 0x0000FF);
                        //}

                    } // end - if (cor>=cor_thres)	
                } // end - for (int j=i+1;j<npixels;j++)			
            } // end - if (mean[i]>=pvalue_thres)
			
            npairs_done+= npixels - i-1;

            time(&t1);
            if (t1-t0>5) {
                double progress = 100.*npairs_done/(filenames.size()-w_size+1)/npairs;
                cerr << round(100*progress)/100 << "% done ";
                cerr << round((t1-t00)/progress*(100-progress)) << " seconds to go. ";
                cerr << endl;
                t0 = t1;
            }
        } // end - for (int i=0;i<npixels;i++)

		img.strokeColor("white"); // Outline color 
		img.strokeWidth(1); // Stroke width
		
		if (strcmp(label, "y") == 0) {
			img.draw(DrawableText(11, 20, frame_number));
		}
		
        view.sync();
        img.write((output_dir + "/" + oss.str()).c_str());

		/****************************************************************/

    }   

	fclose(fpw);

    for (int i=0;i<w_size;i++) {
        if (views[i]!=NULL) {
            delete views[i];
        }
    }

    return 0;
}
