const loanAmountInput = document.querySelector(".loan-amount");
const interestRateInput = document.querySelector(".interest-rate");
const loanTenureInput = document.querySelector(".loan-tenure");

const loanEMIValue = document.querySelector(".loan-emi .value");
const totalInterestValue = document.querySelector(".total-interest .value");
const totalAmountValue = document.querySelector(".total-amount .value");

const calculateBtn = document.querySelector(".calculate-btn");

let loanAmount, interestRate, loanTenure, interest;
let myChart; // Declare the chart variable globally

const checkValues = () => {
  let loanAmountValue = loanAmountInput.value;
  let interestRateValue = interestRateInput.value;
  let loanTenureValue = loanTenureInput.value;

  let regexNumber = /^[0-9]+$/;
  if(!loanAmountValue.match(regexNumber)) {
    loanAmountInput.value = "error";
  }

  if(!loanTenureValue.match(regexNumber)) {
    loanTenureInput.value = "error";
  }

  let regexDecimalNumber = /^(\d*\.)?\d+$/;
  if(!interestRateValue.match(regexDecimalNumber)) {
    interestRateInput.value = "error"
  }
}

const refreshInputValues = () => {
    loanAmount = parseFloat(loanAmountInput.value);
    interestRate = parseFloat(interestRateInput.value);
    loanTenure = parseFloat(loanTenureInput.value);
    interest = interestRate / 12 / 100;
};

const displayChart = (totalInterestPayableValue, loanAmount) => {
    if (myChart) {
        myChart.destroy(); // Destroy previous chart instance if it exists
    }
    const ctx = document.getElementById("myChart").getContext("2d");
    myChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Total Interest", "Principal Loan Amount"],
            datasets: [
                {
                    data: [totalInterestPayableValue, loanAmount],
                    backgroundColor: ["#e63946", "#14213d"],
                    borderWidth: 0,
                },
            ],
        },
    });
};

const updateChart = (totalInterestPayableValue, loanAmount) => {
    myChart.data.datasets[0].data[0] = totalInterestPayableValue;
    myChart.data.datasets[0].data[1] = loanAmount;
    myChart.update();
};

const calculateEMI = () => {
  checkValues();
  refreshInputValues();
  return loanAmount * interest * (Math.pow(1 + interest, loanTenure) / (Math.pow(1 + interest, loanTenure) - 1));
};

const updateData = (emi) => {
    loanEMIValue.innerHTML = Math.round(emi);

    let totalAmount = Math.round(loanTenure * emi);
    totalAmountValue.innerHTML = totalAmount;

    let totalInterestPayable = Math.round(totalAmount - loanAmount);
    totalInterestValue.innerHTML = totalInterestPayable;

    if (myChart) {
        updateChart(totalInterestPayable, loanAmount);
    } else {
        displayChart(totalInterestPayable, loanAmount);
    }
};

const init = () => {
    let emi = calculateEMI();
    updateData(emi);
};

calculateBtn.addEventListener("click", () => {
    refreshInputValues();
    let emi = calculateEMI();
    updateData(emi);
});

init();


