================
Cookiecutter C++
================

.. image:: https://circleci.com/gh/grhawk/cookiecutter-cpp.svg?style=shield
    :target: https://circleci.com/gh/grhawk/cookiecutter-cpp
    :alt: Build Status

Cookiecutter_ template for a C++ package.

* GitHub repo: https://github.com/grhawk/cookiecutter-cpp/
* Documentation (this is for cookiecutter-pypackage): https://cookiecutter-pypackage.readthedocs.io/
* Free software: BSD license


Credits
-------
This is basically a fork of Cookiecutter_.


Features
--------

* Managing dependencies with Conan_ and the CMake-Conan-Integration_. This allows to easily add dependencies directly into the conanfile.txt file.
* Integration of Conan in CLion_.
* No need to execute Conan_ commands (everything run with CMake).
* Provide CLI11_ out-of-the-box (if requested).
* Provide spdlog_ out-of-the-box (if requested).
* Circleci_: Ready for Circleci Continuous Integration testing
* hdoc_ documentation: TODO!
* bump2version_: TODO!

.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter


Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher)::

    pip install -U cookiecutter

Generate a Python package project::

    cookiecutter https://github.com/grhawk/cookiecutter-cpp.git

Enter the newly generated folder. Make sure the Conan_ profile is configured::

    conan profile list

If you don't have a Conan_ profile, you can create one with `conan profile detect --force`.
At this point, according to CMake-Conan-Integration_, you can run::

    mkdir build && cd build;
    cmake -DCMAKE_PROJECT_TOP_LEVEL_INCLUDES=cmake/conan_provider.cmake ..
    cmake --build .

This will prepare the needed C++ libraries and compile the example code.
You can now test the compiled code::

    ./sandbox/cpp_boilerplate-sandbox

and run the unittests::

     ctest


The created folder is already a git repo that you can push on github and has already a basic CI implemented to test
the code with CircleCI.

For more details, see the `cookiecutter-pypackage tutorial`_.

.. _`cookiecutter-pypackage tutorial`: https://cookiecutter-pypackage.readthedocs.io/en/latest/tutorial.html


Not Exactly What You Want?
--------------------------

Don't worry, you have options:

Fork This / Create Your Own
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have differences in your preferred setup, I encourage you to fork this
to create your own version. Or create your own; it doesn't strictly have to
be a fork.

* Once you have your own version working, add it to the Similar Cookiecutter
  Templates list above with a brief description.

* It's up to you whether or not to rename your fork/own version. Do whatever
  you think sounds good.

Contributing
------------

1. Fork the project.
2. Edit whatever you feel like.
3. Describe the changes on the "unreleased" tag in the CHANGELOG.md.
4. Create a Merge Request to the `main` branch.

Once a new branch has been merged, it is enough to create a new semver tag to generate a new version of the cookiecutter repo.


.. _Circleci: http://circleci.com/
.. _Tox: http://testrun.org/tox/
.. _Doxigen: http://doxigen.org/
.. _Read the Docs: https://readthedocs.io/
.. _`pyup.io`: https://pyup.io/
.. _bump2version: https://github.com/c4urself/bump2version
.. _Punch: https://github.com/lgiordani/punch
.. _Poetry: https://python-poetry.org/
.. _PyPi: https://pypi.python.org/pypi
.. _Mkdocs: https://pypi.org/project/mkdocs/
.. _Conan: https://docs.conan.io/1/index.html
.. _CMake-Conan-Integration: https://github.com/conan-io/cmake-conan
.. _hdoc: https://hdoc.io/
.. _CLI11: https://github.com/CLIUtils/CLI11
.. _spdlog: https://github.com/gabime/spdlog
.. _CLion: https://www.jetbrains.com/clion/

.. _`Nekroze/cookiecutter-pypackage`: https://github.com/Nekroze/cookiecutter-pypackage
.. _`tony/cookiecutter-pypackage-pythonic`: https://github.com/tony/cookiecutter-pypackage-pythonic
.. _`ardydedase/cookiecutter-pypackage`: https://github.com/ardydedase/cookiecutter-pypackage
.. _`lgiordani/cookiecutter-pypackage`: https://github.com/lgiordani/cookiecutter-pypackage
.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage
.. _`veit/cookiecutter-namespace-template`: https://github.com/veit/cookiecutter-namespace-template
.. _`zillionare/cookiecutter-pypackage`: https://zillionare.github.io/cookiecutter-pypackage/
.. _github comparison view: https://github.com/tony/cookiecutter-pypackage-pythonic/compare/audreyr:master...master
.. _`network`: https://github.com/audreyr/cookiecutter-pypackage/network
.. _`family tree`: https://github.com/audreyr/cookiecutter-pypackage/network/members

