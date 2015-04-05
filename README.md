#PyMP: A lazy way to make your Python code in parallel

-----

## Installation 

	python setup.py install    

## Sample Use Case

You can make your for-loop run in parallel just by adding "#pragma omp parallel for" near by the for-loop statement, just like what is done by openmp in c language. 

Besides, you need to annotated the outside variables which will be assigned value in the for-loop with annotation "#pragma shared".

### Example Code

For a code is running mandelbrot as follows: 

	def run_mandelbrot(size_x, size_y):
		data = {} 
		
		for row in range(size_x):  
			for col in range(size_y):
				tmp = mandelbrot(row, col, size_x, size_y)
				data[(row, col)] = (tmp[0], tmp[1], tmp[2])
		
		return data
	
All you need is just adding "#pragma omp parallel for" near the for loop, and attaching "#pragma shared" to the variable "data" (because it is outside of for-loop, and it will be assigned value in the loop)

	def run_mandelbrot(size_x, size_y):
		data = {} #pragma shared

		for row in range(size_x):  #pragma omp parallel for
			for col in range(size_y):
				tmp = mandelbrot(row, col, size_x, size_y)
				data[(row, col)] = (tmp[0], tmp[1], tmp[2])
				
		return data

## Dependency 

PyMP used "pathos" package developed by Michael McKerns and his group members. To get more details:

    M.M. McKerns, L. Strand, T. Sullivan, A. Fang, M.A.G. Aivazis,
    "Building a framework for predictive science", Proceedings of
    the 10th Python in Science Conference, 2011;
    http://arxiv.org/pdf/1202.1056

    Michael McKerns and Michael Aivazis,
    "pathos: a framework for heterogeneous computing", 2010- ;
    http://trac.mystic.cacr.caltech.edu/project/pathos