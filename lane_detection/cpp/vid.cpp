#include<iostream>
#include <opencv2/opencv.hpp>
using namespace cv;
int main(int argc, char** argv)
{
  Mat frame;                               //temp image variable
  VideoCapture capture;                    //Array of captured frames
  namedWindow("Window", WINDOW_AUTOSIZE);  //create viewable window/executable
  capture.open(argv[1]);                   //reads input video
  for(;;)
    {
      capture>>frame;                        //amends new frame over previous
      if(frame.empty()) break;               //break if there is no video feed
      imshow("Window",frame);                //display frame in window
      if(waitKey(30)>=0) break;              //Define framerate sampling
    }
  return 0;
}
