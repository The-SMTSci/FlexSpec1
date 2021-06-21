Mathematics
===========

While exploring the physics of optics for the FlexSpec1 we encountered
aspects of mathematics tailored to optics. This section is a collection
of notes that guided our intuition to close the gaps between the theory
and the images we obtained with practice.

- **"Conventions"** get in the way of the pure math.
- **Beware**! Trig **folds** quadrants! 
- Angles are measured as positive in a counter-clockwise direction, and negative in a clockwise direction using the ":index:`right-hand-rule`".

Most calculators and the human brain operate within the social
convention of "degrees". Computer languages, for the most part, work
with radians. High school trigonometry has left most people with a
morbid fear of radians. When radians are used in their simplest terms
they offer a powerful shortcut to intuition for
back-of-the-envelope (:index:`BOTE`) work.

The slope-intercept equation from high school algebra
:index:`equation;slope-intercept` uses a "rise-over-run"
:index:`mathematics;rise-over-run` paradigm that amounts to the
tangent: :math:`sin/cos`. The sin/cos projection winds up inside the
unit circle at the :math:`cos(\theta)` position, while the tangent is
outside the unit circle and goes to infinity as :math:`cos(\theta)
\rightarrow\;0`. The radian measure follows the unit circle and
represents an exact value. The tangent starts at 0 degrees (and
radians) and follows a line tangent to the outside of the unit circle.

Radians
-------

With a spectrograph, the separation between two wavelengths, :math:`\lambda` 
and :math:`\lambda+\Delta{\lambda}` may be calculated by simply (ha!)
differentiating the :index:`grating equation`. The goal is to state
dispersion in units of scale instead of units of wavelength:

.. math::
   :label: ChainRule1

   \frac{\tt{d}\lambda}{\tt{d}x} &= \frac{\tt{d}\lambda}{\tt{d}\beta} \\
               &= \frac{\tt{d}\lambda}{\tt{d}\beta} \frac{\tt{d}\beta}{\tt{d}x} 

where :math:`\tt{d}x` is the distance from the grating towards the
sensor.

The farther the camera lens is from the grating, the higher the resolution
at the cost of dimmer light. 


Angles
------

Angles :index:`Angles;measurement` are measured in a plane, taken as a
counter-clockwise rotation around a normal vector to the plane. In the
Cartesian coordinate system/plane, values start at zero at the
:math:`X` axis and increase as the rotation goes from :math:`X`,
through :math:`Y`. The angle value wraps at zero and repeats. Negative
angles are simply those that move clockwise from zero.

Trigonometric identities "fold values" in their quadrants and pose a
number of computational problems for algorithms. For example,
:math:`Y=sin(X) = 0.5` occurs at both positive and negative
:math:`\pi/6` or 30 degrees. Similarly :math:`Y=cos(X)=0.5` occurs
at :math:`\pi/3` or 60 degrees. In other words, ambiguous results
unless one accounts for circumstances. The cross product returns
a vector normal to the plane of rotation, and with a sign representing
the direction of rotation. The magnitude of the vector can be turned
into exactly one angle. The magnitude of the angle is between :math:`0` and
:math:`pi` BUT the sign allows for the angle to move backwards from zero!
thus :math:`2\pi` - \alpha can take on value :math:`\pi < \alpha < 2\pi`
without confusion.

This angle ambiguity is critical to computing solutions in spectroscopy.

To further complicate things


Small Angle Approximation
-------------------------

Kahan [Kahan-1999]_ recommends the use of vectors over trig for the computation
of small angles.


Estimating accuracy of the :index:`small angle approximation`, taking a
McClaurian series at face value (Taylor's Theorem around :math:`x=0`),

.. math::
   :label: SmallAngleApproximation

    \sin \theta &= \sum^{\infty}_{n=0} \frac{(-1)^n}{(2n+1)!} \theta^{2n+1} \\
       &= x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots\quad\text{ for all } x\! \\


Setting the second term :math:`\;\theta^3\;/\;3! > 1\;/\;206264.8`
gives an error approximation for 1 arcsecond. (There are 206264.8 arc-seconds in a radian.)
Looking for an error of 1 arcsecond and solving for :math:`\theta`:


.. math:: 
    :label: SmallAngleWorked
     \frac{\theta^3}{3!}   &>  4.8481369 \times 10^{-6}   \frac{1}{206064.8} \\
     \theta^3    &> 3! \times  2.9088821 \tt{~ ~ ~ ~ ~ ~ ~ ~}  \times 10^{-5} \:\:\:  (3! = 6) \\
                 &> 6 \times  2.9088821 \tt{~ ~ ~ ~ ~ ~ ~ ~}    \times 10^{-5} \\
        \theta    &> e^{ln \frac{6 \times  2.9088821 \times 10^{-5}}{3}} \tt{~ ~ ~ ~ ~ ~ ~ ~}  \text{ln/3 for cubed root} \\
                 &>  0.0307545 \tt{~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~} \text{[radians]} \\
      \theta      &>\sim 1.76  \tt{~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~}   \text{[degrees] 1 arcsecond error ~3.5 times diameter of Moon} \\
        &>\sim 0.817  \tt{~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~}  \text{[degrees] at one-tenth arcsecond error}


Gaussian
--------

Normalized curves are used to match and measure effective width of
spectral lines. The process of producing a line is Gaussian in nature,
dominated by Maxwell-Boltzmann distribution but influenced by local
physics. Other curves include the Lorenzian and the Voigt profiles.
The Voigt profile is a combination of the Gaussian and lorenzian.
The math related to the Gaussian has aspects that make it attractive
for computation. 

The Gaussian, and a few derivatives are:

.. math::
   :label: Gaussian1

    y(x) &= a exp^\Big(  (\frac{x-\bar{x})^{2}}{\sigma}  \Big) \\
    y^{\prime}(x) &= -\frac{2a(x-\bar{x}}{\sigma}exp^\Big(  (\frac{x-\bar{x})^{2}}{\sigma}  \Big) \\
    y^{\prime\prime}(x) &= 2\frac{a}{\sigma^{2}} \left(-\sigma + 2(x-\bar{x})^{2} \right) exp^\Big(  (\frac{x-\bar{x})^{2}}{\sigma}  \Big)

where :math:`a` is the maximum occurring at :math:`x = \bar{x}`, :math:`\sigma` is
the variance.

The inflection points are minimum at :math:`\bar{x}` and 
maximum at :math:`x=\bar{x}\pm\sqrt{\sigma/2}`.

In general fitting a Gaussian to a PSF for a star, allows cosmic ray
and sensor defects to be corrected -- remembering to account for the
error associated with those corrections.

Derivative:

.. math::
    :label: GaussianDerivative

    \frac{d}{dx} e^{\frac{-ax}{\sigma}}  =  -a/c e^{\frac{-ax}{\sigma}}



Fourier Transform
-----------------

.. math::
    :label: Fourier1

    f(x) &= \int_{-\infty}^{\infty} f(\xi) e^{2 \pi i} \textrm{d}\xi\\

Note:

.. math::
    :label: Fourier2

    e^{2\; \pi i x} = e^{ax}

where :math:`a = 2 \pi i`.

Parallactic Angle
-----------------

The essential aspect of compensating for the parallactic angle is
handled in FlexSpec1 by using the Inertial Measurement Unit of an
include Nano 33 BLE Sense (or IoT) processor. By choosing an axis,
we simply make it 'balanced' w.r.t. the Earth's gravity vector.
A little vector mathematics tells us the minimal direction to rotate
and some book-keeping tells us to avoid cable wrap.











