'''
The theory behind linear regression;

For linear regression (y = mx + b);
m = ((mean(X) x mean(Y)) - mean(X x Y))/((mean(X))^2 - mean(X^2))
b = mean(Y) - (m x mean(X))
'''

from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

xs = np.array([3.733257743, 3.614476954, 0.664183334, 3.890009962, 6.457901254, 2.966391513], dtype=np.float64)
ys = np.array([0.454638784, 0.687226325, 0.071563877, 0.781100766, 1.101155323, 0.323558561], dtype=np.float64)

def best_fit_slope_and_intercept(xs, ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) / ((mean(xs))**2 - mean(xs**2)))
    b = (mean(ys) - (m*mean(xs)))
    return m, b

m, b = best_fit_slope_and_intercept(xs, ys)
print("Slope "+str(m),"Y-Intercept "+str(b))

regression_line = [(m*x) + b for x in xs]
'''
Same as doing:

for x in xs: 
    regression_line.append((m*x) + b)
'''

plt.scatter(xs, ys)
plt.plot(xs, regression_line)
plt.show()

'''
Thoery behind Calculating R^2 Value:

The error is the distance the point is from a line, the error is 
squared to eliminate negatives, and to penalize outliers. 

R^2 = 1 - (Sqaured Error of regression line)/ (Squared Error of mean(ys))                                                               
'''

# My method ,note that ys and regression line are arrays/lists
def r_sq(ys, regression_line):
    return 1 - (sum((ys - regression_line)**2))/(sum((ys - mean(ys))**2))

# Example Method ********************************
def sqaured_error(ys_orig, ys_line):
    return sum((ys_line-ys_orig)**2)

def coe_deter(ys_orig, ys_line):
    y_mean_line = [mean(ys_orig) for y in ys_orig]
    sqaured_error_regr = sqaured_error(ys_orig, ys_line)
    sqaured_error_y_mean = sqaured_error(ys_orig, y_mean_line)
    return 1 - (sqaured_error_regr / sqaured_error_y_mean)

r_squared= coe_deter(ys, regression_line)
r2  = r_sq(ys, regression_line)

print('First'+str(r2))
print('Second'+str(r_squared))



