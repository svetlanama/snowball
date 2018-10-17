#!/usr/bin/env python2
#encoding: UTF-8

# https://newton.cx/~peter/2012/06/poisson-distribution-confidence-intervals/
# Для розподілу Пуассона
# Функція розподілу ймовірностей (cdf) 	
# {\frac {\Gamma (\lfloor k+1\rfloor ,\lambda )}{\lfloor k\rfloor !}}\!{\text{ for }}k\geq 0} 
# (де $\Gamma (x,y)}$ це неповна гамма функція та $\lfloor k\rfloor$ це ціла частина 

from scipy import special

n=14   # number of positive outcomes
a=0.05 # confidence level
N=400  # total number of outcolmes

lower=special.gammaincinv (n, 0.5 * a)/N
upper=special.gammaincinv (n, 1-0.5 * a)/N

print (lower, upper)

if __name__ == "__main__":
    print "Hello World"
