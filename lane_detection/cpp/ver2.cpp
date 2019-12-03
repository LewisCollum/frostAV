#include <iostream>
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/core/fast_math.hpp"
int MAX_KERNEL_LENGTH = 7;
int lowThreshold = 0;
const int max_lowThreshold = 100;
const char* window_name = "Edge Map";
int kernel_size = 3;

int main(int argc, char** argv) {
  cv::Mat src, greyFrame, hsvFrame, newFrame, lowCont, blr, edges, cdst, cdstP;
  cv::VideoCapture capture;
  capture.open(argv[1]);
  for(;;) {
      capture>>src;    
  //std::string path = "tape.jpg";
  // src = cv::imread(path);
  cv::cvtColor(src, hsvFrame, cv::COLOR_BGR2HSV);
  //Isolate Blue Color Lane
  cv::inRange(hsvFrame, cv::Scalar(100,100,100), cv::Scalar(120,255,175), newFrame);
  //Decrease Contrast
  //newFrame.convertTo(lowCont, -1, 0.5, 0);
  //Gaussian Blur
  for (int i=1; i<MAX_KERNEL_LENGTH; i = i+2) {
   cv::GaussianBlur(newFrame, blr, cv::Size(i,i), 0, 0);
   }
  //Edge Detection
  cv::Mat croppedFrame = blr(cv::Rect(0, blr.rows/2, blr.cols, blr.rows/2));
  cv::Canny(croppedFrame, edges, 50, 200, 3);
  cv::cvtColor(edges, cdst, cv::COLOR_GRAY2BGR);
  cdstP = cdst.clone();
  //Area of Interest
  
  // Standard Hough Line Transform
  // std::vector<cv::Vec2f> lines;
  // cv::HoughLines(edges, lines, 1, CV_PI/180, 150, 0, 0 ); 
  // // Draw the lines
  // for( size_t i = 0; i < lines.size(); i++ )
  //    {
  //      float rho = lines[i][0], theta = lines[i][1];
  //      cv::Point pt1, pt2;
  //      double a = cos(theta), b = sin(theta);
  //      double x0 = a*rho, y0 = b*rho;
  //      pt1.x = cvRound(x0 + 1000*(-b));
  //      pt1.y = cvRound(y0 + 1000*(a));
  //      pt2.x = cvRound(x0 - 1000*(-b));
  //      pt2.y = cvRound(y0 - 1000*(a));
  //      cv::line( cdst, pt1, pt2, cv::Scalar(0,0,255), 3, cv::LINE_AA);
  //    }
  // Probabilistic Line Transform
  std::vector<cv::Vec4i> linesP;  // will hold the results of the detection
  cv::HoughLinesP(edges, linesP, 1, CV_PI/180, 50, 50, 10); 
  // Draw the lines
  //std::vector< int > arr; 
  //std::vector<cv::Vec4i> average;
  int averageN=0;
  int averageP=0;
  for ( size_t i = 0; i < linesP.size(); i++ )
     {
       cv::Vec4i l = linesP[i];
       cv::line( cdstP, cv::Point(l[0], l[1]), cv::Point(l[2], l[3]), cv::Scalar(0,0,255), 3, cv::LINE_AA);
       //std::cout<<linesP[i]<<std::endl;
       if (linesP[i][2] <= 640) {
       int slope = (linesP[i][3]-linesP[i][1])/(linesP[i][2]-linesP[i][0]);
       averageN=averageN + slope;
       }
       else {
       int slope = (linesP[i][3]-linesP[i][1])/(linesP[i][2]-linesP[i][0]);
       averageP = averageP + slope;
       }
     }
  //std::cout<<"average negative slope: "<<averageN<<std::endl;
  //std::cout<<"average positive slope: "<<averageP<<std::endl;
  int midslope=0;
  double angle=0;
  if (averageP > abs(averageN)) {
      midslope = averageN - averageP;
  }
  else {
      midslope = averageP - averageN;
   }

  //std::cout<<"Middle Slope: "<<midslope<<std::endl;
  if (midslope < 0) {
      angle = -((CV_PI/2) - atan(abs(midslope)));
  }
  else if (midslope > 0) {
      angle = (CV_PI/2) - atan(midslope);
  }
  else {
      angle = 0;
  }
  std::cout<<angle*180/CV_PI<<std::endl;
  // elsew if (avgSlope < 0) {
      //     angle = 
  //cv::HoughLines
  //clear temp arrays
  //cv::imshow("Std Hough Transfrom", cdst);
  cv::imwrite("./doc/aoi.png", croppedFrame);
  cv::imshow("Prob Hough Transfrom", croppedFrame);
  //cv::waitKey(0);
  if(cv::waitKey(60)>=0) break;
  }
  return 0;
}
