# Codeforces Rating System Simulation

This repository is create for simulating [`Codeforces`](http://codeforces.com) Rating System.

## Usage

~~Sorry for my poor English~~

This python shell required `Python 3` for support. You should ensure the environment PYTH has add Python 3.

What's more, you need to configure with the `MySQL` or other Databases. 

Run the `RatingSystem.py` , and input the `contestId` with `Registered participants` . The Python spider will get the data and stored in DB. (For it linked to Codeforces, please insure to set WaitTime. )

Then, just run `CodeforcesRatingCal.py`, enter a participant nickname and you will get an answer about the RatingChange. (Please remember it is not official and has some deviation)

**Fork or download the sources are welcome.**

## MIT License

Copyright (c) 2017 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

