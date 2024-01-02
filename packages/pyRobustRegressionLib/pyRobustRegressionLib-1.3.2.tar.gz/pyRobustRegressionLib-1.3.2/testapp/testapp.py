#!/bin/env python
"""
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
"""

## Test application. Demonstrates the usage of the library in Python.
## Similar to the test application in c++


# load the library if it is not installed by setuptools (pip) but just compiled by cmake and in the 
# same directory as the python script.
import sys
import os.path
import importlib.util
file_path = os.path.abspath(__file__) 
dir_path = os.path.dirname(file_path) 
sys.path.append(dir_path)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import the robust regression library and it's submodules

import pyRobustRegressionLib as rrl
from pyRobustRegressionLib import StatisticFunctions
from pyRobustRegressionLib import LinearRegression
from pyRobustRegressionLib import MatrixCode 
from pyRobustRegressionLib import LossFunctions
from pyRobustRegressionLib import NonLinearRegression
from pyRobustRegressionLib import RobustRegression

print("\nPrint the description of the sub-modules of pyRobustRegressionLib\n\n")
print(print(rrl.__doc__))


##callback functions that will be given to the c library.
##a fitting function f(X,beta)=beta[0]*X+beta[1], with X as Data and beta as parameters to be found
def linear(X:list, beta:list)->list:
    Y=[]
    for i in range(0,len(X)):
        Y.append(beta[0] * X[i] + beta[1])
    return Y

## The  Jacobi matrix J(X,beta) of the linear function above
def Jacobi(X:list, beta)->rrl.MatrixCode.Matrix:
	m=rrl.MatrixCode.Matrix (len(X), len(beta))
	for i in range(0,len(X)):
		m[i, 0] = X[i]
		m[i, 1] = 1.0
	return m



#custom error function per point. Here the square of the residuals is chosen.
#the residuals are scaled by the pointnumber, in order to avoid that a smaller pointnumber always yields a smaller total error.

def err_pp(Y:float,fY:float,pointnumber:int)->float:
    return ((Y-fY)*(Y-fY))/ float(pointnumber)
#computes the entire error for all points
#           
def aggregate_err(errs:list)->float:
    res=0.0 
    for i in range(0,len(errs)):
        res+=errs[i]
    return res


print("\n\n Now we run some very simple tests.\n\n")
print(""" Some of the algorithms are time consuming. Especially the modified lts/forward-search algorithms.
Therefore, and since this python script is only a demonstration of the function calls of the library
only extremely simple datasets are tried out here that can be written down by hand.
(So for very large data, the iterative outlier removal method may be better suited than the forward search.\n""")



print("\n 5!= ")
print(rrl.StatisticFunctions.factorial(5))
print(rrl.StatisticFunctions.__doc__)

print("\nDefine some array and print it")
X0=[3, 13, 7, 5, 21, 23, 39, 23, 40, 23, 14, 12, 56, 23]

rrl.MatrixCode.Vector(X0).Printvector()

print("compute the median")
print(rrl.StatisticFunctions.median(X0))
print("Compute Q1")
print(rrl.StatisticFunctions.Q1(X0))
print("Compute Q3")
print(rrl.StatisticFunctions.Q3(X0))
print("\nCompute the Standard deviation of the array")
print(rrl.StatisticFunctions.stdeviation(X0))

print("Printing a docstring")
print (rrl.MatrixCode.Identity.__doc__)





m0=rrl.MatrixCode.Identity(3,3)
m1=rrl.MatrixCode.Identity(3,3)
m2=m0+m1



print("\nAddition operator for 2 unit matrices")

m2.Printmatrix()

print("Define a Matrix elementwise")
m3=rrl.MatrixCode.Matrix(3,3)
m3[0, 0] = 1
m3[0, 1] = 2
m3[0, 2] = -1

m3[1, 0] = 1
m3[1, 1] = 1
m3[1, 2] = -1
m3[2, 0] = 2
m3[2, 1] = -1
m3[2, 2] = 1

m3.Printmatrix();

print("Another way to initialize the matrix m in a single line")
m4=rrl.MatrixCode.Matrix(3,3,[1,2,-1,1,1,-1,2,-1,1])
m4.Printmatrix()

v=rrl.MatrixCode.Vector ([2,0,3])

print("Print a vector v with a command")
v.Printvector()


print("\nGaussian algorithm M*res=v")
res=rrl.MatrixCode.Gaussian_algorithm(m3, v)

print("Print the elements of the vector elementwise, maybe floating point conversion effects occur.")
for item in range(0,3):
    print(res[item])


print("\nDefine some arrays X and Y")
X=[-3.0,5.0,7.0,10.0,13.0,16.0,20.0,22.0]
Y=[-210.0,430.0,590.0,830.0,1070.0,1310.0,1630.0,1790.0]

print("\nLoad the arrays into a vector and print them")
Xa=rrl.MatrixCode.Vector(X)
Ya=rrl.MatrixCode.Vector(Y)

Xa.Printvector()
Ya.Printvector()

print("Printing a docstring of a member of a struct")
print(rrl.LinearRegression.result.main_slope.__doc__)

print("\nLinear Regression of X and Y")

res1=rrl.LinearRegression.result()
rrl.LinearRegression.linear_regression(X, Y, res1)


print("Slope") 
print(res1.main_slope)
print("Intercept") 
print(res1.main_intercept)


print("\n\nNow we added 2 outliers. the usual linear regression will not work in this circumstances")

X2=[-3.0, 5.0,7.0, 10.0,13.0,15.0,16.0,20.0,22.0,25.0]
Y2=[ -210.0, 430.0, 590.0,830.0,1070.0,20.0,1310.0,1630.0,1790.0,-3.0]

print("\nLoad the arrays into a vector and print them")
X2a=rrl.MatrixCode.Vector(X2)
Y2a=rrl.MatrixCode.Vector(Y2)

X2a.Printvector()
Y2a.Printvector()


print("\nSimple Linear Regression")
res2=rrl.LinearRegression.result()
rrl.LinearRegression.linear_regression(X2, Y2, res2)
print("Slope") 
print(res2.main_slope)
print("Intercept") 
print(res2.main_intercept)

print("\n\nSiegel's repeated Median Linear Regression")
res3=rrl.LinearRegression.result()
rrl.LinearRegression.median_linear_regression(X2, Y2, res3)
print("Slope") 
print(res3.main_slope)
print("Intercept") 
print(res3.main_intercept)





print("\n\nModified lts algorithm")
ctrl4= rrl.RobustRegression.modified_lts_control_linear()


res4= rrl.RobustRegression.linear_algorithm_result()
rrl.RobustRegression.modified_lts_regression_linear(X2, Y2, ctrl4, res4)

print("Slope") 
print(res4.main_slope)
print("Intercept") 
print(res4.main_intercept)

print("\nOutlier indices")
for ind in res4.indices_of_removedpoints:
    print(ind)


print("\n\nModified lts algorithm, but now instead of the default S estimator with the interquartile range method and the loss function is the absolute value")
ctrl4a= rrl.RobustRegression.modified_lts_control_linear()
ctrl4a.outlier_tolerance=1.5;
ctrl4a.lossfunction=rrl.LossFunctions.absolutevalue
ctrl4a.rejection_method=rrl.RobustRegression.estimator_name.tolerance_is_interquartile_range
res4a= rrl.RobustRegression.linear_algorithm_result()
rrl.RobustRegression.modified_lts_regression_linear(X2, Y2, ctrl4a, res4a)

print("Slope") 
print(res4a.main_slope)
print("Intercept") 
print(res4a.main_intercept)

print("\nOutlier indices")
for ind in res4.indices_of_removedpoints:
    print(ind)






print("\n\n\nIterative outlier with the linear algorithms removal")

ctrl5= rrl.RobustRegression.linear_algorithm_control()
res5= rrl.RobustRegression.linear_algorithm_result()
rrl.RobustRegression.iterative_outlier_removal_regression_linear(X2, Y2, ctrl5, res5)

print("Slope") 
print(res5.main_slope)
print("Intercept") 
print(res5.main_intercept)


print("\nOutlier indices")
for ind in res5.indices_of_removedpoints:
    print(ind)


print("\n\n\nSimple Nonlinear Regression with the original dataset")

res6=rrl.NonLinearRegression.result() 
ctrl6=rrl.NonLinearRegression.control()

init6=rrl.NonLinearRegression.initdata() 
init6.Jacobian=Jacobi
init6.f=linear
init6.initialguess = [1,1]


rrl.NonLinearRegression.non_linear_regression(X, Y, init6, ctrl6, res6)

print("Slope") 
print(res6.beta[0])
print("Intercept") 
print(res6.beta[1])


print("\n\n\nSimple Nonlinear Regression with the modified dataset with outliers")

res6a=rrl.NonLinearRegression.result() 
ctrl6a=rrl.NonLinearRegression.control()

init6a=rrl.NonLinearRegression.initdata() 
init6a.Jacobian=Jacobi
init6a.f=linear
init6a.initialguess = [1,1]


rrl.NonLinearRegression.non_linear_regression(X2, Y2, init6a, ctrl6a, res6a)

print("Slope") 
print(res6a.beta[0])
print("Intercept") 
print(res6a.beta[1])



print("\n\n\nRobust non-linear regression with the same 2 inserted outliers\n")

print("\nIterative outlier removal \n")
res7=rrl.RobustRegression.nonlinear_algorithm_result() 
ctrl7=rrl.RobustRegression.nonlinear_algorithm_control()
init7=rrl.NonLinearRegression.initdata() 
init7.Jacobian=Jacobi
init7.f=linear
init7.initialguess = [1,1]
rrl.RobustRegression.iterative_outlier_removal_regression_nonlinear(X2, Y2, init7, ctrl7, res7)

print("Slope")
print(res7.beta[0])
print("Intercept") 
print(res7.beta[1])

print("\nOutlier indices")
for ind in res7.indices_of_removedpoints:
    print(ind)



print("\n\nModified last trimmed squares\n")
res8=rrl.RobustRegression.nonlinear_algorithm_result() 
ctrl8=rrl.RobustRegression.modified_lts_control_nonlinear()
init8=rrl.NonLinearRegression.initdata() 
init8.Jacobian=Jacobi
init8.f=linear
init8.initialguess = [1,1]
rrl.RobustRegression.modified_lts_regression_nonlinear(X2, Y2, init8, ctrl8, res8)

print("Slope")
print(res8.beta[0])
print("Intercept") 
print(res8.beta[1])


print("\nOutlier indices")
for ind in res8.indices_of_removedpoints:
    print(ind)


print("\n\nModified last trimmed squares with a custom error function\n")
res9=rrl.RobustRegression.nonlinear_algorithm_result() 
ctrl9=rrl.RobustRegression.modified_lts_control_nonlinear()
ctrl9.lossfunction=rrl.LossFunctions.custom
ctrl9.loss_perpoint=err_pp
ctrl9.aggregate_err=aggregate_err

init9=rrl.NonLinearRegression.initdata() 
init9.Jacobian=Jacobi
init9.f=linear
init9.initialguess = [1,1]
rrl.RobustRegression.modified_lts_regression_nonlinear(X2, Y2, init9, ctrl9, res9)

print("Slope")
print(res9.beta[0])
print("Intercept") 
print(res9.beta[1])

print("\nOutlier indices")
for ind in res9.indices_of_removedpoints:
    print(ind)
