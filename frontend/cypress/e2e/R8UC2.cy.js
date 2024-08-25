describe('Test cases for R8UC2', () => {
  let uid;
  let email;
  let task_id;
  let todo_id;

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
    cy.fixture("NewTask.json").then(task => {
      task.userid = uid;
      cy.request({
        method: "POST",
        url: "http://localhost:5000/tasks/create",
        form: true,
        body: task
      }).then(response => {
        task_id = response.body[0]._id.$oid;
        todo_id = response.body[0].todos[0]._id.$oid;
      });
    });
  });
  beforeEach(function() {
    cy.visit('http://localhost:3000');
    cy.contains('div', 'Email Address').find('input[type=text]').type(email);
    cy.get('form').submit();
    cy.get('.title-overlay').last().click();
    cy.wait(2000);
  });

  // Test case 1: Verify that a todo item can be marked as done when the user clicks on the checkbox icon
  it('Test case 1: Verify that a todo item can be marked as done when the user clicks on the checkbox icon.', () => {
    const data = `data={'$set': {'done': false}}`;
    cy.request({
      method: 'PUT',
      url: `http://localhost:5000/todos/byid/${todo_id}`,
      body: data,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    cy.get('.todo-list .todo-item')
      .eq(0)
      .find('[class^=checker]')
      .trigger('click', { force: true }) // Uncheck the checkbox
      .wait(200);

    cy.get('.todo-list .todo-item')
      .eq(0)
      .find('[class^=checker]')
      .should('have.class', 'checked');
  });

  // Test case 2: Verify that a todo item can be marked as active when the user clicks on the checkbox icon again
  it('Test case 2: Verify that a todo item can be marked as active when the user clicks on the checkbox icon again.', () => {
    const data = `data={'$set': {'done': true}}`;
    cy.request({
      method: 'PUT',
      url: `http://localhost:5000/todos/byid/${todo_id}`,
      body: data,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    cy.get('.todo-list .todo-item')
      .eq(0)
      .find('[class^=checker]')
      .trigger('click', { force: true })
      .wait(200);

    cy.get('.todo-list .todo-item')
      .eq(0)
      .find('[class^=checker]')
      .should('have.class', 'unchecked');
  });
  after(function () {
    cy.request({
      method: 'DELETE',
      url: `http://localhost:5000/users/${uid}`
    }).then((response) => {
      cy.log(response.body);
    });
  });
});