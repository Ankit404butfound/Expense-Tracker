import React, { useEffect, useRef, useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

var curstate = false;
const ExpenseForm = () => {
  const [date, setDate] = useState(null);
  const [itemName, setItemName] = useState("");
  const [amount, setAmount] = useState("");
  const [purchasedBy, setPurchasedBy] = useState("");
  const [savedData, setSavedData] = useState([]);
  useEffect(() => {
    /*
    Query logic
    */
    if (!curstate) {
      console.log("i fire once");
      fetch("/get_expenses")
        .then((response) => {
          return response.json();
        })
        .then((jsonData) => {
          for (const key in jsonData.expenses) {
            setSavedData((prevData) => [
              ...prevData,
              {
                date: jsonData.expenses[key].purchase_date,
                itemName: jsonData.expenses[key].item_name,
                amount: jsonData.expenses[key].amount,
                purchasedBy: jsonData.expenses[key].purchased_by,
              },
            ]);
          }
        });

      curstate = true;
    }
  }, []);
  const handleChange = (selectedDate) => {
    setDate(selectedDate);
  };
  const handleSaveData = () => {
    if (
      date == null ||
      itemName == null ||
      amount == null ||
      purchasedBy == null
    ) {
      return;
    } else {
      const newData = {
        date: date,
        itemName: itemName,
        amount: amount,
        purchasedBy: purchasedBy,
      };
      console.log(date, itemName, amount, purchasedBy);
      var xhttp = new XMLHttpRequest();
      xhttp.open(
        "GET",
        `/add_expense?item_name=${itemName}&amount=${amount}&purchased_by=${purchasedBy}&purchase_date=${date
          .toString()
          .split(" ")
          .slice(0, 4)
          .join(" ")}`,
        true
      );
      xhttp.send();

      setSavedData((prevData) => [...prevData, newData]);
      setDate(null);
      setItemName("");
      setAmount("");
      setPurchasedBy("");
    }
  };

  return (
    <>
      <div className="container">
        <nav className="navbar bg-primary">
          <div className="container-fluid">
            <h1 className="navbar-brand">Room-Expense Tracker</h1>
          </div>
        </nav>
      </div>
      <div className="input-field">
        <div className="row g-4">
          <div className="col-sm-6">
            <input
              type="text"
              className="form-control"
              placeholder="Item Name"
              value={itemName}
              onChange={(e) => setItemName(e.target.value)}
            />
          </div>
          <div className="col-sm">
            <input
              type="number"
              className="form-control"
              placeholder="Amount"
              aria-label="State"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
            />
          </div>
          <div className="col-sm">
            <select
              className="form-control"
              id="dropdownSelect"
              value={purchasedBy}
              onChange={(e) => setPurchasedBy(e.target.value)}
            >
              <option value="">Purchased By</option>
              <option value="Dhruv">Dhruv</option>
              <option value="Ankit">Ankit</option>
              <option value="Ayush">Ayush</option>
            </select>
          </div>
          <div className="col-sm">
            <DatePicker
              className="form-control"
              selected={date}
              onChange={handleChange}
              placeholderText="Purchase Date"
            />
          </div>
          <div className="col-sm">
            <button
              className=" btn btn-success form-control"
              onClick={handleSaveData}
            >
              Save
            </button>
          </div>
          {savedData.length > 0 && (
            <div>
              <h3>Expenses</h3>
              <table>
                <thead>
                  <tr>
                    <th> Date </th>
                    <th>Item Name</th>
                    <th>Amount</th>
                    <th>Purchased By</th>
                  </tr>
                </thead>
                <tbody>
                  {savedData.map((data, index) => (
                    <tr key={index}>
                      <td>
                        {data.date.toString().split(" ").slice(0, 4).join(" ")}
                      </td>
                      <td>{data.itemName}</td>
                      <td>{data.amount}</td>
                      <td>{data.purchasedBy}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </>
  );
};

export default ExpenseForm;
