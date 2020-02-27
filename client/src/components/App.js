import React from "react";
import "../css/App.css";
import Table from "./table/Table";
class App extends React.Component {
  state = {
    data: [],
    loadingFinished: false,
    error: ''
  };

  componentDidMount() {
    this.fetchData();
  }

  async fetchData () {    
      const res = await fetch(`${process.env.REACT_APP_API_ROOT_URL}trades/`)
      if (!res.ok){
        return this.setState({error: 'Something went wrong while retrieving trades.', loadingFinished: true})
      } 
      const jsonData = await res.json()
      this.setState({data: jsonData, loadingFinished: true})
  }

  renderData(data){
    if (this.state.error === ''){
      return <Table data={data}  />
    } 
    return <p>{this.state.error}</p>
  } 

  render() {
    const { data, loadingFinished } = this.state;
    return (
      <div>
        {loadingFinished ? (
            <div style={{ marginTop: "50px", marginBottom: "20px", width: "60%", margin: "0 auto" }}>
                <h1>Booked trades</h1>
                <hr />
                {this.renderData(data)} 
            </div>
        ) : (
            <p>Loading....</p>
          )}
      </div>
    );
  }
}

export default App;
