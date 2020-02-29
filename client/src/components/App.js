import React from "react";
import "../css/App.css";
import Table from "./table/Table";

class App extends React.Component {
    state = {
        tableData: [],
        currencies: ["EUR", "USD"],
        selectedCurrencies: {
            sell: "EUR",
            buy: "",
        },
        rate: 0,
        sellAmount: 1000,
        loadingFinished: false,
        showCreateTrade: false,
        error: ''
    };

    componentDidMount() {
        this.fetchTableData();
        this.fetchCurrencies();
    }

    async fetchTableData() {
        const res = await fetch(`${process.env.REACT_APP_API_ROOT_URL}trades/`);
        if (!res.ok) {
            return this.setState({
                error: 'Something went wrong while retrieving trades.',
                loadingFinished: true
            })
        }
        const jsonData = await res.json();
        this.setState({tableData: jsonData, loadingFinished: true})
    }

    async fetchCurrencies() {
        const res = await fetch(`${process.env.REACT_APP_API_ROOT_URL}currencies/`);
        const jsonData = await res.json();
        const currencies = jsonData.map(object => (object.name));
        this.setState({currencies: currencies})
    }

    async fetchRate() {
        const res = await fetch(
            `${process.env.REACT_APP_API_ROOT_URL}rates/?sell=${this.state.selectedCurrencies.sell}&buy=${this.state.selectedCurrencies.buy}`);
        const jsonData = await res.json();
        this.setState({rate: jsonData.rate})
    }

    renderTable(data) {
        if (this.state.error === '') {
            return <Table data={data}/>
        }
        return <p>{this.state.error}</p>
    }

    generateCurrencyOptions(currencies) {
        return (
            currencies.map(currency => (<option key={currency}>{currency}</option>))
        )
    }

    limitDecimalPlaces(e, count) {
      if (e.target.value.indexOf('.') === -1) { return; }
      if ((e.target.value.length - e.target.value.indexOf('.')) > count) {
        e.target.value = parseFloat(e.target.value).toFixed(count);
      }
    }

    setCurrentSellCurrency(event) {
        this.setState({
            ...this.state,
            selectedCurrencies: {
                ...this.state.selectedCurrencies,
                sell: event.target.value
            }
        }, () => {
            if (this.state.selectedCurrencies.sell && this.state.selectedCurrencies.buy) {
                this.fetchRate()
            }
        });

    }

    setCurrentBuyCurrency(event) {
        this.setState({
            selectedCurrencies: {
                ...this.state.selectedCurrencies, buy: event.target.value
            }
        }, () => {
            if (this.state.selectedCurrencies.sell && this.state.selectedCurrencies.buy) {
                this.fetchRate()
            }
        });

    }

    cancelCreate() {
        this.setState({
            rate: 0,
            sellAmount: 0,
            selectedCurrencies: {
                sell: "",
                buy: ""
            }
        })
    }

    renderCreateTrade() {
        this.setState({showCreateTrade: true})
    }

    createTrade() {
        const payload = {
            sell_currency: this.state.selectedCurrencies.sell,
            sell_amount: this.state.sellAmount,
            buy_currency: this.state.selectedCurrencies.buy,
            buy_amount: (this.state.rate * this.state.sellAmount).toFixed(2),
            rate: this.state.rate
        };

        fetch(`${process.env.REACT_APP_API_ROOT_URL}trades/`, {
            method: 'post',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        })
            .then(() => {
                this.fetchTableData()
            })
    }

    render() {
        const {tableData, loadingFinished} = this.state;
        const selectedCurrencies = Object.values(this.state.selectedCurrencies);
        const sellOptions = this.state.currencies.filter(
            currency => !selectedCurrencies.find(
                sP => sP === currency) || currency === this.state.selectedCurrencies.sell);
        const buyOptions = this.state.currencies.filter(
            currency => !selectedCurrencies.find(
                sP => sP === currency) || currency === this.state.selectedCurrencies.buy);
        return (
            <div>
                {loadingFinished ? (
                    <div style={{
                        marginTop: "50px",
                        marginBottom: "20px",
                        width: "60%",
                        margin: "0 auto"
                    }}>
                        <div style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "center"
                        }}><h1>Booked trades</h1>
                            <div>
                                <button type="button" onClick={() => this.renderCreateTrade()}>New
                                    Trade
                                </button>
                            </div>
                        </div>
                        <hr/>
                        {this.renderTable(tableData)}
                    </div>
                ) : (
                    <p>Loading....</p>
                )}
                {this.state.showCreateTrade &&
                <div style={{width: "60%", margin: "50px auto 10px auto"}}>
                    <h1>New Trade</h1>
                    <hr/>
                    <div style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "flex-start"
                    }}>

                        <div>
                            <label htmlFor="name">Sell Currency</label><br/>
                            <select id="sell-currency" style={{width: "100%"}}
                                    value={this.state.selectedCurrencies.sell}
                                    onChange={(event) => {
                                        this.setCurrentSellCurrency(event)
                                    }}>
                                <option/>
                                {this.generateCurrencyOptions(sellOptions)}
                            </select>
                            <label htmlFor="name">Sell Amount</label><br/>
                            <input id="sell-input" type="number" step=".01" name="sell"
                                   onInput={(event) => this.limitDecimalPlaces(event, 2)}
                                   onChange={
                                       (event) => this.setState({sellAmount: event.target.value})
                                   }/>

                        </div>
                        <div>
                            <label htmlFor="name">Rate</label><br/>
                            <label>{this.state.rate}</label>
                        </div>
                        <div>
                            <label htmlFor="name">Buy Currency</label><br/>
                            <select id="buy-currency" style={{width: "100%"}}
                                    value={this.state.selectedCurrencies.buy}
                                    onChange={(event) => {
                                        this.setCurrentBuyCurrency(event)
                                    }}>
                                <option/>
                                {this.generateCurrencyOptions(buyOptions)}
                            </select>
                            <label htmlFor="name">Buy Amount</label><br/>
                            <input id="buy-input" type="number" step=".01" name="buy" disabled="disabled"
                                   value={(this.state.rate * this.state.sellAmount).toFixed(2)}
                                   readOnly/>

                        </div>


                    </div>
                    <div style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "flex-start",
                        marginTop: "20px"
                    }}>
                        <button type="button"
                                disabled={!(this.state.selectedCurrencies.sell
                                    && this.state.selectedCurrencies.buy
                                    && this.state.sellAmount)}
                                onClick={() => {
                                    this.createTrade()
                                }}>
                            Create
                        </button>
                        <button type="button"
                                onClick={() => {
                                    this.cancelCreate()
                                }}>
                            Cancel
                        </button>
                    </div>
                </div>}

            </div>
        );
    }
}

export default App;
