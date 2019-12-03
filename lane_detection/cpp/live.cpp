#include "opencv2/opencv.hpp"

int main(int argc, char** argv)
{
    cv::VideoCapture capture;
    if(!capture.open(0)) return 0;
    while(1) {
        cv::Mat frame;
        capture >> frame;
        if(frame.empty()) break;
          
        cv::imshow("this is you, smile! :)", frame);
        if(cv::waitKey(10) == 27) break;
    }
    //capture.close();
    return 0;
}
