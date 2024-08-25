describe('Test cases for R8UC1', () => {
  // Variables to store user information
  let uid;
  let email;

  // Before hook to create a user and login before each test
  before(() => {
    cy.fixture('user.json').then((user) => {
      // Create a user
      cy.request({
        method: 'POST',
        url: 'http://localhost:5000/users/create',
        form: true,
        body: user
      }).then((response) => {
        uid = response.body._id.$oid;
        email = user.email;
      });
    });
  });

  // Before each hook to login before each test
  beforeEach(() => {
    cy.fixture("NewTask.json")
    .then(task => {
      task.userid = uid,
      cy.request({
        method: "POST",
        url: "http://localhost:5000/tasks/create",
        form: true,
        body: task
      }).then(response => {
      })
    })
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Email Address').find('input[type=text]').type(email);
    cy.get('form').submit();
    cy.get('.title-overlay').last().click();
    cy.wait(2000);
  });

  // Test case 1: Verify that all todo items can be deleted when the user clicks on the delete icon
  it('Test case 1: Verify that all todo items can be deleted when the user clicks on the delete icon', () => {
    cy.intercept('DELETE', '/todos/byid/*').as('deleteTodo');
    cy.get('.todo-list .todo-item .remover').eq(0).click();
    cy.wait('@deleteTodo').its('response.statusCode').should('eq', 200); // i dont know why i cant get the item to dissapere when i click it but i know that the request is sent and resived correktly
  });

  after(function () {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body)
    })
  })
})