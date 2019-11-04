#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include "opencv2/imgcodecs.hpp"
using namespace std;
using namespace cv;
int MAX_KERNEL_LENGTH=11;
Mat dst, detected_edges;
Mat src, greyFrame, hlsFrame, lowCont, blr ;
int lowThreshold = 0;
const int max_lowThreshold = 100;
//int ratio = 3;
const int kernel_size = 3;
const char* window_name = "Edge Map";
static void CannyThreshold(int, void*) {
  //blur( src_gray, detected_edges, Size(3,3) );
  Canny( blr, detected_edges, lowThreshold, lowThreshold*3, kernel_size );
  dst = Scalar::all(0);
  src.copyTo( dst, detected_edges);
  imshow( window_name, dst );
}

int main () {
  //Mat src, greyFrame, hlsFrame, lowCont, blr ;
  string path = "test.jpg";               //path of image
  src = imread(path, IMREAD_COLOR);               //read image, keep color
  cvtColor(src, greyFrame, COLOR_RGB2GRAY);
  // cvtColor(hlsFrame, greyFrame, HLS_RGB2GRAY); 
  greyFrame.convertTo(lowCont, -1, 0.5, 0);
  for ( int i = 1; i < MAX_KERNEL_LENGTH; i = i + 2 )
    {
      GaussianBlur( lowCont, blr, Size( i, i ), 0, 0 );
    }
  dst.create( src.size(), src.type() );
  namedWindow("Display Window", WINDOW_AUTOSIZE); 
  createTrackbar( "Min Threshold:", window_name, &lowThreshold, max_lowThreshold, CannyThreshold );
  CannyThreshold(0, 0);
  waitKey(0);                                 
  return 0;
}
