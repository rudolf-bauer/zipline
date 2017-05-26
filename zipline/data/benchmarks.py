#
# Copyright 2013 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import pandas as pd
import pandas_datareader as pdr

from six.moves.urllib_parse import urlencode


def format_yahoo_index_url(symbol, start_date, end_date):
    """
    Format a URL for querying Yahoo Finance for Index data.
    """
    return (
        'https://ichart.finance.yahoo.com/table.csv?' + urlencode({
            's': symbol,
            # start_date month, zero indexed
            'a': start_date.month - 1,
            # start_date day
            'b': start_date.day,
            # start_date year
            'c': start_date.year,
            # end_date month, zero indexed
            'd': end_date.month - 1,
            # end_date day
            'e': end_date.day,
            # end_date year
            'f': end_date.year,
            # daily frequency
            'g': 'd',
        })
    )


def get_benchmark_returns(symbol, start_date, end_date, source='google'):
    """
    Get a Series of benchmark returns from Yahoo.

    Returns a Series with returns from (start_date, end_date].

    start_date is **not** included because we need the close from day N - 1 to
    compute the returns for day N.
    """
    return pdr.data.DataReader(symbol, source, start_date, end_date).sort_index().tz_localize('UTC').pct_change(1).iloc[1:]