/*

Copyright(c) < 2023 > <Benjamin Schulz>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files(the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and /or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions :

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#pragma once
#include <valarray>
#include <stdint.h>
#include "robustregressionlib_exports.h"

using namespace std;

namespace Statisticfunctions
{
	//Computes the absolute value of f
	ROBUSTREGRESSION_API double fabs(double f);

	//Computes the factorial n!
	ROBUSTREGRESSION_API double factorial(size_t n);

	//Computes the standard deviation of an array
	ROBUSTREGRESSION_API double stdeviation(valarray<double>& errs);

	//Computes the average of an array
	ROBUSTREGRESSION_API double average(valarray<double>& errs);

	//Computes the median of an array 
	ROBUSTREGRESSION_API double median(valarray<double> arr );

	//Computes the low median of an array
	ROBUSTREGRESSION_API double lowmedian(valarray<double> arr);

	//Computes the student t distribution for a significance level alpha and an array of size nu from the algorithm in
	// Smiley W. Cheng, James C. Fu, Statistics & Probability Letters 1 (1983), 223-227

	ROBUSTREGRESSION_API double t(double alpha, size_t nu);

	//Computes the critical values of the student t distribution for significance level alpha and an array of size N
	ROBUSTREGRESSION_API double crit(double alpha, size_t N);

	//Computes the peirce criterium from the point number, the number of outliers and the number of parameters to be fitted.
	//see https://en.wikipedia.org/wiki/Peirce%27s_criterion for an introduction and references to Peirce's original article in
	// B. Peirce  Astronomical Journal II 45 (1852) 
	ROBUSTREGRESSION_API double peirce(size_t pointnumber, size_t numberofoutliers, size_t fittingparameters);

	//Computes the binomial coefficient n over k
	ROBUSTREGRESSION_API size_t binomial(size_t n, size_t k);


	// Computes the Q estimator of Croux and Rousseuuw for an array.
	// The estimator was published in
	// Peter J. Rousseeuw, Christophe Croux, Alternatives to the Median-Absolute Deviation
	// J. of the Amer. Statistical Assoc. (Theory and Methods), 88 (1993),p. 1273,
	// Croux, C., Rousseeuw, P.J. (1992). Time-Efficient Algorithms for Two Highly Robust Estimators of Scale.
	// In: Dodge, Y., Whittaker, J. (eds) Computational Statistics. Physica, Heidelberg.
	// https://doi.org/10.1007/978-3-662-26811-7_58 
	ROBUSTREGRESSION_API double Q_estimator(valarray<double>& err );

	//Computes the S estimator of rousseuuw for an array. 
	//The estimator was published in 
	// Peter J. Rousseeuw, Christophe Croux, Alternatives to the Median-Absolute Deviation
	// J. of the Amer. Statistical Assoc. (Theory and Methods), 88 (1993),p. 1273, and
	// Croux, C., Rousseeuw, P.J. (1992). Time-Efficient Algorithms for Two Highly Robust Estimators of Scale.
	// In: Dodge, Y., Whittaker, J. (eds) Computational Statistics. Physica, Heidelberg.
	// https://doi.org/10.1007/978-3-662-26811-7_58 (For the faster version of the S-estimator.)
	// The version of the S estimator in this library now is adapted from Croux and Rousseeuw to the C language. 
	//Note that it is not the same Code because of some optimizations. Since many variables act on array indices in this algorithm,
	// it was actually non-trivial to convert from Fortran to C.
	ROBUSTREGRESSION_API double S_estimator(valarray<double>& err);

	// Computes the MAD estimator. It needs the median of the array. The coefficients in front of the MAD used here were found in
	// Croux, C., Rousseeuw, P.J. (1992). Time-Efficient Algorithms for Two Highly Robust Estimators of Scale.
	// In: Dodge, Y., Whittaker, J. (eds) Computational Statistics. Physica, Heidelberg.
	// https://doi.org/10.1007/978-3-662-26811-7_58 (For the faster version of the S-estimator.)
	ROBUSTREGRESSION_API double MAD_estimator(valarray<double>& err, double& m);

	//Computes the t estimator of an array.
	// The estimator was described in
	// Peter J. Rousseeuw, Christophe Croux, Alternatives to the Median-Absolute Deviation
	// J. of the Amer. Statistical Assoc. (Theory and Methods), 88 (1993),p. 1273,
	ROBUSTREGRESSION_API double T_estimator(valarray<double>& err);

	//Computes the biweight midvariance for one step for an array,
	//  It expects the median m of the array. The estimator is described in 
	//   T. C. Beers,K. Flynn and K. Gebhardt,  Astron. J. 100 (1),32 (1990)
	ROBUSTREGRESSION_API double onestepbiweightmidvariance(valarray<double>& err, double& m);

	//Compute the Quartile Q3
	ROBUSTREGRESSION_API double Q3(valarray<double> m);
	//Computes the Quartile Q1
	ROBUSTREGRESSION_API double Q1(valarray<double> m);
}
