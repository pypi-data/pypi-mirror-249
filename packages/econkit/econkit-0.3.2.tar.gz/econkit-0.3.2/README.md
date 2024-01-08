<h1>EconKit Package</h1>

<p>This is a detailed description of the EconKit package. It provides advanced tools and functions for econometric analysis, tailored to the needs of researchers, students, and professionals in economics and finance.</p>

<h2>Installation</h2>

<p>To install the EconKit package, run the following command:</p>

<pre><code>pip install econkit</code></pre>

<h2>Usage</h2>

<p>Here's how to use the main functions in the package:</p>

<pre><code>### EXAMPLE ###

## Import Libraries ##
from econkit import descriptives
from econkit import correlation
from econkit import stock
from econkit import table


### Run ###

# 1. Download Stock Information #
# 1.1 Stocks #
stock1 = 'ETE.AT'
stock2 = 'LAVI.AT'
stock3 = 'TPEIR.AT'
stock4 = 'EKTER.AT'
stock5 = 'TRESTATES.AT'
stock6 = 'INKAT.AT'
stock7 = 'EXAE.AT'


# 1.2 Preiod #
start = '01-12-2022'
end = '30-12-2023'

# 1.3 Frequency #
freq = '1d'

# 1.4 Function #
stock(stock1, start, end, freq)
stock(stock2, start, end, freq)
stock(stock3, start, end, freq)
stock(stock4, start, end, freq)
stock(stock5, start, end, freq)
stock(stock6, start, end, freq)
stock(stock7, start, end, freq)


# 2. Combine Multiple Stocks' Returns into One Table #
Returns = table('Returns', ETE, LAVI, TPEIR, EKTER, TRESTATES, INKAT, EXAE)

# 3. Find Useful Statistics, such as Expected Values, Standard Deviation,... "
descriptives(Returns)
correlation(Returns, method="Spearman", p="T")
</code></pre>

<h2>Features</h2>

<ul>
  <li>Comprehensive econometric analysis tools</li>
  <li>Support for various correlation methods</li>
  <li>User-friendly interface for complex statistical operations</li>
</ul>

<h2>Requirements</h2>

<p>The package requires the following Python libraries:</p>

<ul>
  <li>Numpy</li>
  <li>Pandas</li>
  <li>Scipy</li>
</ul>

<h2>Contributing</h2>

<p>We welcome contributions to the EconKit package. Please read the contributing guidelines before submitting your pull requests.</p>

<h2>License</h2>

<p>This project is licensed under the BSD 3-Clause License - see the <a href="LICENSE">LICENSE</a> file for details.</p>

<h2>Acknowledgments</h2>

<p>Special thanks to all contributors and supporters of the project.</p>

<h2>Contact</h2>

<p>For questions or support, please contact <a href="mailto:contact@stfanstavrianos.eu">contact@stfanstavrianos.eu</a>.</p>

