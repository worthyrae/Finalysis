import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
import seaborn as sns
import yfinance as yf
import statsmodels.api as sm
from statsmodels import regression

def main():
    st.sidebar.write('''
             Get Equity Data
             ''')
    names = pd.read_csv('secwiki_tickers.csv')
    names = names.dropna()
    c_date = date.today()
    ticker = st.sidebar.selectbox("Select Ticker", names['Ticker'].tolist())
    period = st.sidebar.selectbox("Select Period", ["1 Week", "1 Month", "3 Months", "6 Months", "9 Months", "1 Year", "3 Years", "5 Years"])
    if period == "1 Week":
        start_d = c_date - timedelta(7)
    elif period == "1 Month":
        start_d = c_date - timedelta(30)
    elif period == "3 Months":
        start_d = c_date - timedelta(90)
    elif period == "6 Months":
        start_d = c_date - timedelta(180)
    elif period == "9 Months":
        start_d = c_date - timedelta(270)
    elif period == "1 Year":
        start_d = c_date - timedelta(365)
    elif period == "3 Years":
        start_d = c_date - timedelta(365*3)
    elif period == "5 Years":
        start_d = c_date - timedelta(365*5)
    if st.sidebar.button('display'):
        c1, c2 = st.beta_columns([1, 3])
        stock_data = yf.Ticker(ticker)
        company_name = stock_data.info['shortName']
        for index, row in names.iterrows():
            if str(row['Ticker']) == str(ticker):
                company_sector = row['Sector']
        price_data = stock_data.history(start=start_d, end=c_date, interval="1d")
        price_data['Return'] = (price_data['Close'] / price_data['Open'] - 1) * 100
        t0 = price_data['Open'][0]
        tn = price_data['Close'][len(price_data['Close'])-1]
        percent_change = (tn / t0 - 1)*100
        cp_pc = f"${tn:,.2f}" + f" ({percent_change:,.2f}%)"
        c1.write(company_name)
        c1.write(cp_pc)
        fig, ax = plt.subplots()
        ax.plot(price_data['Close'].index, price_data['Close'])
        ax.xaxis.set_major_locator(plt.MaxNLocator(4))
        ax.set_ylabel("$ per Share")
        ax.set_title(f"{ticker} {period} Stock Performance")
        c2.pyplot(fig)
        ptb = stock_data.info['priceToBook']
        with st.beta_expander("Benchmark Comparison"):
            c3, c4 = st.beta_columns([1, 3])
            benchmark_data = yf.Ticker("SPY")
            benchmark_price_data = benchmark_data.history(start=start_d, end=c_date, interval="1d")
            benchmark_price_data['Return'] = (benchmark_price_data['Close'] / benchmark_price_data['Open'] - 1) * 100
            b_t0 = benchmark_price_data['Open'][0]
            b_tn = benchmark_price_data['Close'][len(benchmark_price_data['Close'])-1]
            b_percent_change = round((b_tn / b_t0 - 1)*100, 2)
            b_cp_pc = "SPY" + " (" + f"{b_percent_change:,.2f}" + "%)"
            c3.write("Returns")
            s_comp = ticker + f" ({percent_change:,.2f}%)"
            delta = percent_change - b_percent_change
            c3.write(s_comp)
            c3.write(b_cp_pc)
            c3.write(f"Delta ({delta:.2f}%)")
            c3.write("")
            c3.write("Statistics")
            x = sm.add_constant(benchmark_price_data['Return'])
            y = price_data['Return']
            model = regression.linear_model.OLS(y,x).fit()
            alpha = model.params[0]
            beta = model.params[1]
            c3.write(f"Alpha {alpha:.2f}")
            c3.write(f"Beta {beta:.2f}")
            b_fig, b_ax = plt.subplots()
            b_ax.plot(price_data['Return'].index, price_data['Return'], label=f"{ticker}")
            b_ax.plot(benchmark_price_data['Return'].index, benchmark_price_data['Return'], label="SPY")
            b_ax.xaxis.set_major_locator(plt.MaxNLocator(4))
            b_ax.set_ylabel("% Return")
            b_ax.set_title(f"Benchmark % Return Comparison Over {period}")
            b_ax.legend()
            c4.pyplot(b_fig)
        with st.beta_expander("Company Financials"):
            c7, c8 = st.beta_columns([2, 2])
            try:
                dividend_rate = stock_data.info['dividendRate']
                if dividend_rate != None:
                    c7.write("Dividend Rate")
                    c8.write(f"{dividend_rate:.2f}%")
            except:
                pass
            try:
                sma200 = stock_data.info['twoHundredDayAverage']
                if sma200 != None:
                    c7.write("SMA200")
                    c8.write(f"${sma200:,.2f}")
            except:
                pass
            try:
                sma50 = stock_data.info['fiftyDayAverage']
                if sma50 != None:
                    c7.write("SMA50")
                    c8.write(f"${sma50:,.2f}")
            except:
                pass
            try:
                high = stock_data.info['fiftyTwoWeekHigh']
                if high != None:
                    c7.write("Yearly High")
                    c8.write(f"${high:,.2f}")
            except:
                pass
            try:
                low = stock_data.info['fiftyTwoWeekLow']
                if low != None:
                    c7.write("Yearly Low")
                    c8.write(f"${low:.2f}")
            except:
                pass
            try:
                volume = stock_data.info['volume']
                if volume != None:
                    c7.write("Current Volume")
                    c8.write(f"{volume:,}")
            except:
                pass
            try:
                average_volume = stock_data.info['averageVolume']
                if average_volume != None:
                    c7.write("Average Volume")
                    c8.write(f"{average_volume:,}")
            except:
                pass
            try:
                market_cap = stock_data.info['marketCap']
                if market_cap != None:
                    c7.write("Market Capitalization")
                    c8.write(f"${market_cap:,}")
            except:
                pass
            try:
                shares_outstanding = stock_data.info['sharesOutstanding']
                if shares_outstanding != None:
                    c7.write("Shares Outstanding")
                    c8.write(f"{shares_outstanding:,}")
            except:
                pass
            try:
                shares_short = stock_data.info['sharesShort']
                if shares_short != None:
                    c7.write("Shares Short")
                    c8.write(f"{shares_short:,}")
            except:
                pass
            try:
                book_value = stock_data.info['bookValue']
                if book_value != None:
                    c7.write("Book Value Per Share")
                    c8.write(f"${book_value:,.2f}")
            except:
                pass
            try:
                price_to_book_value = stock_data.info['priceToBook']
                if price_to_book_value != None:
                    c7.write("Price to Book Ratio")
                    c8.write(f"{price_to_book_value:,.2f}")
            except:
                pass
            try:
                enterprise_value = stock_data.info['enterpriseValue']
                if enterprise_value != None:
                    c7.write("Enterprise Value")
                    c8.write(f"${enterprise_value:,}")
            except:
                pass
            try:
                enterprise_revenue_value = stock_data.info['enterpriseToRevenue']
                if enterprise_revenue_value != None:
                    c7.write("Enterprise to Revenue Ratio")
                    c8.write(f"{enterprise_revenue_value:,.2f}")
            except:
                pass
            try:
                enterprise_ebitda_value = stock_data.info['enterpriseToEbitda']
                if enterprise_ebitda_value != None:
                    c7.write("Enterprise to EBITDA Ratio")
                    c8.write(f"{enterprise_ebitda_value:,.2f}")
            except:
                pass
            try:
                forward_eps = stock_data.info['forwardEps']
                if forward_eps != None:
                    c7.write("Forward Eearnings Per Share")
                    c8.write(f"${forward_eps:,.2f}")
            except:
                pass
            try:
                trailing_eps = stock_data.info['trailingEps']
                if trailing_eps != None:
                    c7.write("Trailing Earnings Per Share")
                    c8.write(f"${trailing_eps:,.2f}")
            except:
                pass
            try:
                forward_pe = stock_data.info['forwardPE']
                if forward_pe != None:
                    c7.write("Forward Price to Earnings Ratio")
                    c8.write(f"{forward_pe:,.2f}")
            except:
                pass
            try:
                trailing_pe = stock_data.info['trailingPE']
                if trailing_pe != None:
                    c7.write("Trailing Price to Earnings Ratio")
                    c8.write(f"{trailing_pe:,.2f}")
            except:
                pass
            try:
                profit_margin = stock_data.info['profitMargins']
                if profit_margin != None:
                    profit_margin = profit_margin * 100
                    c7.write("Profit Margin")
                    c8.write(f"{profit_margin:.2f}%")
            except:
                pass
        with st.beta_expander(f"Sector Comparison ({company_sector})"):
            progress_counter = 0
            progress_bar = st.progress(progress_counter)
            c5, c6 = st.beta_columns([1, 3])
            industry_return_list = []
            gainers_list = []
            losers_list = []
            for index, row in names.iterrows():
                if str(row['Sector']) == str(company_sector):
                    i_ticker = row['Ticker']
                    industry_stock_data = yf.Ticker(i_ticker)
                    industry_price_data = industry_stock_data.history(start=start_d, end=c_date, interval="1d")
                    try:
                        i_t0 = industry_price_data['Open'][0]
                    except:
                        continue
                    try:
                        i_tn = industry_price_data['Close'][len(industry_price_data['Close'])-1]
                    except:
                        continue
                    i_percent_change = (i_tn / i_t0 - 1)*100
                    industry_return_list.append(i_percent_change)
                    if len(gainers_list) != 5:
                        gainers_list.append((i_percent_change, i_ticker))
                    else:
                        gainers_list.append((i_percent_change, i_ticker))
                        if min(gainers_list) == (i_percent_change, i_ticker):
                            gainers_list.remove((i_percent_change, i_ticker))
                        else:
                            gainers_list.remove(min(gainers_list))
                    if len(losers_list) != 5:
                        losers_list.append((i_percent_change, i_ticker))
                    else:
                        losers_list.append((i_percent_change, i_ticker))
                        if max(losers_list) == (i_percent_change, i_ticker):
                            losers_list.remove((i_percent_change, i_ticker))
                        else:
                            losers_list.remove(max(losers_list))
                progress_counter += (1/len(names))
                progress_bar.progress(progress_counter)
            gainers_list = sorted(gainers_list, reverse=True)
            losers_list = sorted(losers_list)
            progress_bar.progress(100)
            c5.write("Gainers")
            g_counter = 1
            for item in gainers_list:
                g_ticker = item[1]
                g_return = item[0]
                c5.write(f"{g_counter}. {g_ticker} ({g_return:,.2f}%)")
                g_counter += 1
            c5.write("")
            c5.write("Performance")
            c5.write(f"{ticker} ({percent_change:,.2f}%)")
            c5.write("Losers")
            l_counter = 1
            for item in losers_list:
                l_ticker = item[1]
                l_return = item[0]
                c5.write(f"{l_counter}. {l_ticker} ({l_return:,.2f}%)")
                l_counter += 1
            industry_return_mean = sum(industry_return_list) / len(industry_return_list)
            industry_return_variance = sum([((x - industry_return_mean) ** 2) for x in industry_return_list]) / len(industry_return_list)
            industry_return_std = industry_return_variance ** 0.5
            industry_return_list_wo_outliers = []
            for item in industry_return_list:
                if industry_return_mean-2*industry_return_std <= item <= industry_return_mean+2*industry_return_std:
                    industry_return_list_wo_outliers.append(item)
            industry_return_mean_wo_outliers = sum(industry_return_list_wo_outliers) / len(industry_return_list_wo_outliers)
            industry_return_variance_wo_outliers = sum([((x - industry_return_mean_wo_outliers) ** 2) for x in industry_return_list_wo_outliers]) / len(industry_return_list_wo_outliers)
            industry_return_std_wo_outliers = industry_return_variance_wo_outliers ** 0.5
            i_fig, i_ax = plt.subplots()
            i_ax = sns.kdeplot(industry_return_list_wo_outliers, shade=True)
            i_ax = plt.axvline(industry_return_mean_wo_outliers, color='g', label="Mean")
            i_ax = plt.axvline(percent_change, color='c', label=f"{ticker}")
            i_ax = plt.MaxNLocator(4)
            i_ax = plt.legend()
            i_ax = plt.xlabel("% Return")
            i_ax = plt.ylabel("Probability")
            i_ax = plt.title(f"Distribution of Sector % Returns Over {period}")
            c6.pyplot(i_fig)
            c6.write(f"Mean ({industry_return_mean_wo_outliers:,.2f}%)")
            c6.write(f"Standard Deviation ({industry_return_std_wo_outliers:,.2f}%)")


if __name__ == '__main__':
    main()
