#include <stdio.h>
#include <stdlib.h>

int which_int (double x, double *sv, int nv)
{
	int i;
	for (i=0;i<nv;i++)
	{
		if (x <= sv[i+1])
			return i;
	}
	return -1;
}
/*
// plot the Rauzy fractal of the word w in the numpy array im, for the projection V
void rauzy_fractal_plot (int *w, int n, PyArrayObject *V, PyArrayObject *im)
{
	// test that im has the correct dimensions
    if (im->nd != 2)
    {
        printf("Error: numpy array im must be two-dimensional (here %d-dimensional).", im->nd);
        return;
    }
    if (im->strides[1] != 4)
    {
        printf("Error: pixels must be stored with 4 bytes (RGBA format). Here %ld bytes/pixel.", im->strides[1]);
        return;
    }
    // test that V has correct dimensions
    if (V->nd != 2)
    {
        printf("Error: numpy array V must be two-dimensional (here %d-dimensional).", V->nd);
        return;
    }
    if (V->dimensions[0] != 2)
    {
    	printf("Error: the projection V must be to dimension 2 (here {}).", V->dimensions[0]);
    }
    
    int sx = im->dimensions[1];
    int sy = im->dimensions[0];
    int na = V->dimensions[1]; // taille de l'alphabet
    double *v = (double *)malloc(sizeof(double)*na);
    int i;
    for (i=0;i<na;i++)
    {
    	v[i] = 0;
    }
    //double *x = (double *)
    
    
    // TODO !!!!
    
}
*/

void CETn (double x, double *v, int nv, double tau, int niter, double **proj, int dp, double *xmp)
{
	double *sv = (double *)malloc(sizeof(double)*(nv+1));
	int i, j, k;
	double s = 0;
	//printf("[");
	for (i=0;i<nv;i++)
	{
		//printf("%lf, ", s);
		sv[i] = s;
		s += v[i];
	}
	//printf("%lf]\n", s);
	sv[nv] = s;
	int *p = (int *)malloc(sizeof(int)*nv);
	for (i=0;i<nv;i++)
	{
		p[i] = 0;
	}
	double *xp = (double *)malloc(sizeof(double)*dp); // current point
	//double *xmp = (double *)malloc(sizeof(double)*dp); // minimum point
	for (i=0;i<dp;i++)
	{
		xp[i] = 0;
		xmp[i] = 1./0.;
	}
	//printf("iterate...\n");
	// iterate the CETn
	for (i=0;i<niter;i++)
	{
		x = x - (int)x;
		//printf("x=%lf\n", x);
		j = which_int(x, sv, nv);
		//printf("j = %d\n", j);
		if (j < 0)
		{
			printf("Error : %ld is not in an intervalle !\n", x);
		}
		p[j]++;
		for (k=0;k<dp;k++)
		{
			xp[k] += proj[j][k];
			if (xp[k] < xmp[k])
				xmp[k] = xp[k];
		}
		x = sv[j]+sv[j+1] - x + tau;
	}
	//printf("free...\n");
	free(xp);
	free(p);
	free(sv);
}
