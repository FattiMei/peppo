*> \brief <b> DGTSV computes the solution to system of linear equations A * X = B for GT matrices </b>
*
*  =========== DOCUMENTATION ===========
*
* Online html documentation available at
*            http://www.netlib.org/lapack/explore-html/
*
*> Download DGTSV + dependencies
*> <a href="http://www.netlib.org/cgi-bin/netlibfiles.tgz?format=tgz&filename=/lapack/lapack_routine/dgtsv.f">
*> [TGZ]</a>
*> <a href="http://www.netlib.org/cgi-bin/netlibfiles.zip?format=zip&filename=/lapack/lapack_routine/dgtsv.f">
*> [ZIP]</a>
*> <a href="http://www.netlib.org/cgi-bin/netlibfiles.txt?format=txt&filename=/lapack/lapack_routine/dgtsv.f">
*> [TXT]</a>
*
*  Definition:
*  ===========
*
*       SUBROUTINE DGTSV( N, NRHS, DL, D, DU, B, LDB, INFO )
*
*       .. Scalar Arguments ..
*       INTEGER            INFO, LDB, N, NRHS
*       ..
*       .. Array Arguments ..
*       DOUBLE PRECISION   B( LDB, * ), D( * ), DL( * ), DU( * )
*       ..
*
*
*> \par Purpose:
*  =============
*>
*> \verbatim
*>
*> DGTSV  solves the equation
*>
*>    A*X = B,
*>
*> where A is an n by n tridiagonal matrix, by Gaussian elimination with
*> partial pivoting.
*>
*> Note that the equation  A**T*X = B  may be solved by interchanging the
*> order of the arguments DU and DL.
*> \endverbatim
*
*  Arguments:
*  ==========
*
*> \param[in] N
*> \verbatim
*>          N is INTEGER
*>          The order of the matrix A.  N >= 0.
*> \endverbatim
*>
*> \param[in] NRHS
*> \verbatim
*>          NRHS is INTEGER
*>          The number of right hand sides, i.e., the number of columns
*>          of the matrix B.  NRHS >= 0.
*> \endverbatim
*>
*> \param[in,out] DL
*> \verbatim
*>          DL is DOUBLE PRECISION array, dimension (N-1)
*>          On entry, DL must contain the (n-1) sub-diagonal elements of
*>          A.
*>
*>          On exit, DL is overwritten by the (n-2) elements of the
*>          second super-diagonal of the upper triangular matrix U from
*>          the LU factorization of A, in DL(1), ..., DL(n-2).
*> \endverbatim
*>
*> \param[in,out] D
*> \verbatim
*>          D is DOUBLE PRECISION array, dimension (N)
*>          On entry, D must contain the diagonal elements of A.
*>
*>          On exit, D is overwritten by the n diagonal elements of U.
*> \endverbatim
*>
*> \param[in,out] DU
*> \verbatim
*>          DU is DOUBLE PRECISION array, dimension (N-1)
*>          On entry, DU must contain the (n-1) super-diagonal elements
*>          of A.
*>
*>          On exit, DU is overwritten by the (n-1) elements of the first
*>          super-diagonal of U.
*> \endverbatim
*>
*> \param[in,out] B
*> \verbatim
*>          B is DOUBLE PRECISION array, dimension (LDB,NRHS)
*>          On entry, the N by NRHS matrix of right hand side matrix B.
*>          On exit, if INFO = 0, the N by NRHS solution matrix X.
*> \endverbatim
*>
*> \param[in] LDB
*> \verbatim
*>          LDB is INTEGER
*>          The leading dimension of the array B.  LDB >= max(1,N).
*> \endverbatim
*>
*> \param[out] INFO
*> \verbatim
*>          INFO is INTEGER
*>          = 0: successful exit
*>          < 0: if INFO = -i, the i-th argument had an illegal value
*>          > 0: if INFO = i, U(i,i) is exactly zero, and the solution
*>               has not been computed.  The factorization has not been
*>               completed unless i = N.
*> \endverbatim
*
*  Authors:
*  ========
*
*> \author Univ. of Tennessee
*> \author Univ. of California Berkeley
*> \author Univ. of Colorado Denver
*> \author NAG Ltd.
*
*> \ingroup gtsv
*
*  =====================================================================
      SUBROUTINE dgtsv( N, NRHS, DL, D, DU, B, LDB, INFO )
*
*  -- LAPACK driver routine --
*  -- LAPACK is a software package provided by Univ. of Tennessee,    --
*  -- Univ. of California Berkeley, Univ. of Colorado Denver and NAG Ltd..--
*
*     .. Scalar Arguments ..
      INTEGER            INFO, LDB, N, NRHS
*     ..
*     .. Array Arguments ..
      DOUBLE PRECISION   B( LDB, * ), D( * ), DL( * ), DU( * )
*     ..
*
*  =====================================================================
*
*     .. Parameters ..
      DOUBLE PRECISION   ZERO
      parameter( zero = 0.0d+0 )
*     ..
*     .. Local Scalars ..
      INTEGER            I, J
      DOUBLE PRECISION   FACT, TEMP
*     ..
*     .. Intrinsic Functions ..
      INTRINSIC          abs, max
*     ..
*     .. External Subroutines ..
      EXTERNAL           xerbla
*     ..
*     .. Executable Statements ..
*
      info = 0
      IF( n.LT.0 ) THEN
         info = -1
      ELSE IF( nrhs.LT.0 ) THEN
         info = -2
      ELSE IF( ldb.LT.max( 1, n ) ) THEN
         info = -7
      END IF
      IF( info.NE.0 ) THEN
         CALL xerbla( 'DGTSV ', -info )
         RETURN
      END IF
*
      IF( n.EQ.0 )
     $   RETURN
*
      IF( nrhs.EQ.1 ) THEN
         DO 10 i = 1, n - 2
            IF( abs( d( i ) ).GE.abs( dl( i ) ) ) THEN
*
*              No row interchange required
*
               IF( d( i ).NE.zero ) THEN
                  fact = dl( i ) / d( i )
                  d( i+1 ) = d( i+1 ) - fact*du( i )
                  b( i+1, 1 ) = b( i+1, 1 ) - fact*b( i, 1 )
               ELSE
                  info = i
                  RETURN
               END IF
               dl( i ) = zero
            ELSE
*
*              Interchange rows I and I+1
*
               fact = d( i ) / dl( i )
               d( i ) = dl( i )
               temp = d( i+1 )
               d( i+1 ) = du( i ) - fact*temp
               dl( i ) = du( i+1 )
               du( i+1 ) = -fact*dl( i )
               du( i ) = temp
               temp = b( i, 1 )
               b( i, 1 ) = b( i+1, 1 )
               b( i+1, 1 ) = temp - fact*b( i+1, 1 )
            END IF
   10    CONTINUE
         IF( n.GT.1 ) THEN
            i = n - 1
            IF( abs( d( i ) ).GE.abs( dl( i ) ) ) THEN
               IF( d( i ).NE.zero ) THEN
                  fact = dl( i ) / d( i )
                  d( i+1 ) = d( i+1 ) - fact*du( i )
                  b( i+1, 1 ) = b( i+1, 1 ) - fact*b( i, 1 )
               ELSE
                  info = i
                  RETURN
               END IF
            ELSE
               fact = d( i ) / dl( i )
               d( i ) = dl( i )
               temp = d( i+1 )
               d( i+1 ) = du( i ) - fact*temp
               du( i ) = temp
               temp = b( i, 1 )
               b( i, 1 ) = b( i+1, 1 )
               b( i+1, 1 ) = temp - fact*b( i+1, 1 )
            END IF
         END IF
         IF( d( n ).EQ.zero ) THEN
            info = n
            RETURN
         END IF
      ELSE
         DO 40 i = 1, n - 2
            IF( abs( d( i ) ).GE.abs( dl( i ) ) ) THEN
*
*              No row interchange required
*
               IF( d( i ).NE.zero ) THEN
                  fact = dl( i ) / d( i )
                  d( i+1 ) = d( i+1 ) - fact*du( i )
                  DO 20 j = 1, nrhs
                     b( i+1, j ) = b( i+1, j ) - fact*b( i, j )
   20             CONTINUE
               ELSE
                  info = i
                  RETURN
               END IF
               dl( i ) = zero
            ELSE
*
*              Interchange rows I and I+1
*
               fact = d( i ) / dl( i )
               d( i ) = dl( i )
               temp = d( i+1 )
               d( i+1 ) = du( i ) - fact*temp
               dl( i ) = du( i+1 )
               du( i+1 ) = -fact*dl( i )
               du( i ) = temp
               DO 30 j = 1, nrhs
                  temp = b( i, j )
                  b( i, j ) = b( i+1, j )
                  b( i+1, j ) = temp - fact*b( i+1, j )
   30          CONTINUE
            END IF
   40    CONTINUE
         IF( n.GT.1 ) THEN
            i = n - 1
            IF( abs( d( i ) ).GE.abs( dl( i ) ) ) THEN
               IF( d( i ).NE.zero ) THEN
                  fact = dl( i ) / d( i )
                  d( i+1 ) = d( i+1 ) - fact*du( i )
                  DO 50 j = 1, nrhs
                     b( i+1, j ) = b( i+1, j ) - fact*b( i, j )
   50             CONTINUE
               ELSE
                  info = i
                  RETURN
               END IF
            ELSE
               fact = d( i ) / dl( i )
               d( i ) = dl( i )
               temp = d( i+1 )
               d( i+1 ) = du( i ) - fact*temp
               du( i ) = temp
               DO 60 j = 1, nrhs
                  temp = b( i, j )
                  b( i, j ) = b( i+1, j )
                  b( i+1, j ) = temp - fact*b( i+1, j )
   60          CONTINUE
            END IF
         END IF
         IF( d( n ).EQ.zero ) THEN
            info = n
            RETURN
         END IF
      END IF
*
*     Back solve with the matrix U from the factorization.
*
      IF( nrhs.LE.2 ) THEN
         j = 1
   70    CONTINUE
         b( n, j ) = b( n, j ) / d( n )
         IF( n.GT.1 )
     $      b( n-1, j ) = ( b( n-1, j )-du( n-1 )*b( n, j ) ) / d( n-1 )
         DO 80 i = n - 2, 1, -1
            b( i, j ) = ( b( i, j )-du( i )*b( i+1, j )-dl( i )*
     $                  b( i+2, j ) ) / d( i )
   80    CONTINUE
         IF( j.LT.nrhs ) THEN
            j = j + 1
            GO TO 70
         END IF
      ELSE
         DO 100 j = 1, nrhs
            b( n, j ) = b( n, j ) / d( n )
            IF( n.GT.1 )
     $         b( n-1, j ) = ( b( n-1, j )-du( n-1 )*b( n, j ) ) /
     $                       d( n-1 )
            DO 90 i = n - 2, 1, -1
               b( i, j ) = ( b( i, j )-du( i )*b( i+1, j )-dl( i )*
     $                     b( i+2, j ) ) / d( i )
   90       CONTINUE
  100    CONTINUE
      END IF
*
      RETURN
*
*     End of DGTSV
*
      END

