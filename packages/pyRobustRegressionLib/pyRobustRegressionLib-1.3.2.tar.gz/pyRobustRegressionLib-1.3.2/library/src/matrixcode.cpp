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

#include <iostream>
#include <valarray>
#include <execution>
#include <omp.h>
#include "matrixcode.h"
#include <type_traits>
using signed_size_t = std::make_signed_t<std::size_t>;
using namespace std;




ROBUSTREGRESSION_API   Vector::Vector(const size_t s) {
	m.resize(s, 0.0);
}

ROBUSTREGRESSION_API   Vector::Vector(valarray<double> *m1)
{
	m = *m1;
}
ROBUSTREGRESSION_API   Vector::Vector(const valarray<double> m1)
{
	m = m1;
}

ROBUSTREGRESSION_API  void Vector::Resize(const size_t t)
{
	m.resize(t);
}

ROBUSTREGRESSION_API  Vector Vector::operator=(Vector& B)
{
	size_t s = B.Size();
	m.resize(s);

	for (size_t j = 0; j < s;j++)
	{
		m[j] = B(j);
	}
	return *this;
}


ROBUSTREGRESSION_API  Vector Vector::operator=(Vector* B)
{
	m = *B;
	return *this;
}

ROBUSTREGRESSION_API  Vector Vector::operator+(const Vector& B) const{
	Vector sum(m.size());

#pragma omp simd
	for (size_t i = 0; i < m.size(); i++)
	{
		sum(i) = m[i] + B(i);
	}
	return sum;
}
ROBUSTREGRESSION_API  Vector Vector::operator -(const Vector& B)const {
	Vector sum(m.size());

#pragma omp simd
	for (signed_size_t i = 0; i < m.size(); i++)
	{
		sum(i) = m[i] - B(i);
	}
	return sum;
}
ROBUSTREGRESSION_API  double Vector::operator*(const Vector& B)const {
	double sum = 0;
#pragma omp simd
	for (size_t i = 0; i < m.size(); i++)
	{
		sum += m[i] * B(i);
	}
	return sum;
}


ROBUSTREGRESSION_API  Vector Vector::operator*(const double& B)const {
	Vector sum(m.size());

	for (size_t i = 0; i < m.size(); i++)
	{
		sum(i) = m[i] * B;
	}
	return sum;
}
ROBUSTREGRESSION_API  Vector Vector::operator/(const double& B) const{
	Vector sum(this->Size());
	if (B != 0)
	{
		for (size_t i = 0; i < m.size(); i++)
		{
			sum(i) = m[i] / B;
		}
	}
	return sum;
}

ROBUSTREGRESSION_API  double& Vector::operator()(const size_t i)
{
	return  m[i];
}


ROBUSTREGRESSION_API  const double& Vector::operator()(const size_t i)const
{
	return m[i];
}


 inline size_t  Vector::Size()const
{
	return  m.size();
}


 ROBUSTREGRESSION_API  void Matrixcode::printvector(const Vector &v)
 {
	 for (size_t i = 0; i < v.Size(); i++)
	 {
		 cout << v(i) << " ";
	 }
	 cout << endl;
 }


 ROBUSTREGRESSION_API  Matrix::Matrix (const size_t rows, const size_t columns, valarray<double> m1)
  {
	  r = rows;
	  c = columns;
	  m = m1;
  }

 ROBUSTREGRESSION_API  Matrix::Matrix(const size_t rows, const size_t columns, valarray<double>* m1)
  {
	  r = rows;
	  c = columns;
	  m = *m1;
  }

 ROBUSTREGRESSION_API  Matrix::Matrix(const size_t rows, const size_t columns) {
	 r = rows;
	 c = columns;
	 m.resize(r * c, 0.0);
 }


ROBUSTREGRESSION_API   Matrix Matrixcode::Identity(const size_t rows, const size_t columns)
{
	Matrix m(rows, columns);
	for (size_t i = 0; i < rows; i++)
	{
		if (i < columns)
		{
			m(i, i) = 1.0;
		}
	}
	return m;
}
ROBUSTREGRESSION_API  Matrix Matrixcode::Diagonal(const Matrix &m) 
{
	size_t u = m.Rows();
	Matrix m1(u, m.Columns());
	for (size_t i = 0; i < u; i++)
	{
		m1(i, i) = m(i, i);
	}
	return m1;
}
ROBUSTREGRESSION_API  Vector Matrixcode::Gaussian_algorithm(const Matrix &m,const  Vector& v)
{
	  return (Vector)Matrixcode::Gaussian_algorithm(m,(valarray<double>)v);
}

ROBUSTREGRESSION_API  void Matrix::SwapRows(const size_t row1, const size_t row2) 
{

	  if (row1 != row2) 
	  {
		  for (size_t j = 0; j < c; j++) {
			  std::swap(m[row1 *c + j], m[row2 * c + j]);
		  }
	  }

  }






ROBUSTREGRESSION_API  valarray<double> Matrixcode::Gaussian_algorithm(const Matrix &m, const  valarray<double>& v)
  {
		size_t u = m.Rows();
		size_t t = m.Columns();

		Matrix m2(u, t + 1);

		for (size_t i = 0; i < u; i++)
		{
			for (size_t j = 0; j < t; j++)
			{
				m2(i, j) = m(i, j);
			}
			m2(i, t) = v[i];
		}

		valarray<double>result(v.size());

		for (size_t j = 0; j < t; j++)
		{
			size_t pivot_row = j;
			for (size_t i = j + 1; i < u; i++)
			{
				if (std::abs(m2(i, j)) > std::abs(m2(pivot_row, j))) {
					pivot_row = i;
				}
			}

			if (pivot_row != j)
				m2.SwapRows(j, pivot_row);

			double pivot_value = m2(j, j);
			for (size_t k = j; k < t + 1; k++)
			{
				m2(j, k) /= pivot_value;
			}

			for (size_t i = j + 1; i < u; i++)
			{
				double factor = m2(i, j);

				for (size_t k = j; k < t + 1; k++) 
				{
					m2(i, k) -= factor * m2(j, k);
				}
			}
		}


		for (size_t i = t; i > 0; i--) 
		{
			double sum = 0.0;
			for (size_t j = (size_t)i; j < t; j++) {
				sum += m2(i-1, j) * result[j];
			}
			result[i-1] = (m2(i-1, t) - sum);
		}

		return result;
}
 



ROBUSTREGRESSION_API  void Matrix::Resize(const size_t rows,const size_t columns)
{
	r = rows;
	c = columns;
	m.resize(r * c, 0.0);
}

ROBUSTREGRESSION_API  Matrix Matrix::operator+(const Matrix& B) const{
	Matrix sum(c, r);
	for (signed_size_t i = 0; i < r; i++)
	{
		for (size_t j = 0; j < c; j++)
		{
			sum(i, j) = (*this)(i, j) + B(i, j);
		}
	}
	return sum;
}

ROBUSTREGRESSION_API   Matrix Matrix::operator-(const Matrix& B) const{
	Matrix diff(r, c);
	for (signed_size_t i = 0; i < r; i++)
	{
		for (size_t j = 0; j < c; j++)
		{
			diff(i, j) = (*this)(i, j) - B(i, j);
		}
	}

	return diff;
}

ROBUSTREGRESSION_API  Matrix Matrix::operator*(const Matrix& B) const{
	Matrix multip(r, B.Columns());

	if (c == B.Rows())
	{
		for (long i = 0; i < r; i++)
		{
			for (size_t j = 0; j < B.Columns(); j++)
			{
				double temp = 0.0;
#pragma omp simd
				for (size_t k = 0; k < c; k++)
				{
					temp += (*this)(i, k) * B(k, j);
				}
				multip(i, j) = temp;
			}
		}
	}
	return multip;
}

ROBUSTREGRESSION_API  Matrix Matrix::operator*(const double& scalar) const{
	Matrix result(r, c);
	for (signed_size_t i = 0; i < r; i++)
	{
		for (size_t j = 0; j < c; j++)
		{
			result(i, j) = (*this)(i, j) * scalar;
		}
	}
	return result;
}

ROBUSTREGRESSION_API  Vector Matrix::operator*(const Vector& B)const {

	Vector result((this)->Rows());
	if (B.Size() == (this)->Columns())
	{
		for (signed_size_t i = 0; i < r; i++)
		{
			double sum = 0;
#pragma omp simd
			for (size_t j = 0; j < c; j++)
			{
				sum += (*this)(i, j) * B(j);
			}
			result(i) = sum;
		}
	}
	return result;
}

ROBUSTREGRESSION_API  valarray<double> Matrix::operator*(const valarray<double>& B) const{

	valarray<double> result((this)->Rows());

	if (B.size() == (this)->Columns())
	{
		for (signed_size_t i = 0; i < r; i++)
		{
			double sum = 0;
#pragma omp simd
			for (size_t j = 0; j < c; j++)
			{
				sum += (*this)(i, j) * B[j];
			}
			result[i] = sum;
		}
	}
	return result;
}



ROBUSTREGRESSION_API  Matrix Matrix::operator/(const double&scalar) const {
	Matrix result(r, c);

	for (signed_size_t i = 0; i < r; i++)
	{
		for (size_t j = 0; j < c; j++)
		{
			result(i, j) = (*this)(i, j) / scalar;
		}
	}
	return result;
}


ROBUSTREGRESSION_API  double& Matrix::operator()(const size_t i, const  size_t j)
{
	return  m[i * c + j];
}


ROBUSTREGRESSION_API  const double& Matrix::operator()(const size_t i, const  size_t j)const
{
	return m[i * c + j];
}



ROBUSTREGRESSION_API  size_t Matrix::Rows() const
{
	return this->r;
}

ROBUSTREGRESSION_API  size_t Matrix::Columns() const
{
	return this->c;
}

ROBUSTREGRESSION_API  Matrix Matrixcode::Transpose(const Matrix &m)
{
	size_t c = m.Columns();
	size_t r = m.Rows();
	Matrix t(c, r);
	for (signed_size_t i = 0; i < c; i++)
	{
		for (size_t j = 0; j < r; j++)
		{
			t(i, j) = m(j, i);
		}
	}
	return t;
}

ROBUSTREGRESSION_API  void Matrixcode::printmatrix(const Matrix &m)
{
	for (signed_size_t i = 0; i < m.Rows(); i++)
	{
		for (size_t j = 0; j < m.Columns(); j++)
		{
			cout << m(i, j) << " ";
		}
		cout << endl;
	}
	cout << endl;
}
