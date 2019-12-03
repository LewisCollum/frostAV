#include <iostream>
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/core/fast_math.hpp"
int MAX_KERNEL_LENGTH = 7;
int lowThreshold = 0;
const int max_lowThreshold = 100;
int kernel_size = 3;
const char* window_name = "Edge Map";
int main() {
  cv::Mat src, greyFrame, hsvFrame, newFrame, lowCont, blr;
  std::string path = "tape.jpg";
  src = cv::imread(path, cv::IMREAD_COLOR);
  cv::cvtColor(src, hsvFrame, cv::COLOR_BGR2HSV);
  cv::namedWindow("Display Window", cv::WINDOW_AUTOSIZE);
  cv::inRange(hsvFrame, cv::Scalar(100,100,100), cv::Scalar(110,255,150), newFrame);
  //newFrame.convertTo(lowCont, -1, 0.5, 0);
   for (int i=1; i<MAX_KERNEL_LENGTH; i = i+2) {
     cv::GaussianBlur(newFrame, blr, cv::Size(i,i), 0, 0);
   }
  cv::Mat dst, detected_edges, cdst, cdstP;
  //cv::cvtColor(blr, dst, COLOR_BGR2GRAY); 
  //blr.create(src.size(), src.type());
  // cv::createTrackbar("Min Threshold:", window_name, &lowThreshold,  max_lowThreshold, CannyThreshold);
  //cv::Canny(blr, detected_edges, lowThreshold, lowThreshold*3, kernel_size );
  //dst = cv::Scalar::all(0);
  //src.copyTo(detected_edges, c);
  //cv::cvtColor(detected_edges, cdst, cv::COLOR_BGR2GRAY);
  //cv::blur( img_ori, img_blur, cv::Size(5,5) );
  //cv::Canny(img_blur, img_edge, 100, 150, 3);
  cdstP = cdst.clone();
  
  /* 
  std::vector<cv::Vec2f> lines;
  cv::HoughLines(dst, lines, 1, CV_PI/180, 100, 0, 0 );
  for( size_t i = 0; i < lines.size(); i++ )
    {
      float rho = lines[i][0], theta = lines[i][1];
      cv::Point pt1, pt2;
      double a = cos(theta), b = sin(theta);
      double x0 = a*rho, y0 = b*rho;
      pt1.x = cvRound(x0 + 1000*(-b));
      pt1.y = cvRound(y0 + 1000*(a));
      pt2.x = cvRound(x0 - 1000*(-b));
      pt2.y = cvRound(y0 - 1000*(a));
      cv::line( detected_edges, pt1, pt2, cv::Scalar(0,0,255), 3, cv::LINE_AA);
    }
 */ 

  
  std::vector<cv::Vec4i> linesP; // will hold the results of the detection
  cv::HoughLinesP(detected_edges, linesP, 1, CV_PI/180, 50, 50, 10 ); //runs the actual detection
  for( size_t i = 0; i < linesP.size(); i++ ) {
    cv::Vec4i l = linesP[i];
    cv::line( cdstP, cv::Point(l[0], l[1]), cv::Point(l[2], l[3]), cv::Scalar(0,0,255), 3, cv::LINE_AA);
    }
  

  if (!cdst.data)
    {
      std::cout << "Image not loaded";
      return -1;
    }
  
  //cv::imshow(window_name, cdst);
  //cv::imshow("Display Window", cdst);
  //imshow("Source", src);
  //imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst);
  imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP);
  cv::waitKey(0);
  return(0);
}
