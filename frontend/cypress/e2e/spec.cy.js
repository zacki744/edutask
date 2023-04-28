describe('Open the login page', () => {
  //fixtures
  let uid
  let name

  beforeEach(() => {
  
    //create fabricated user from fixture
    cy.fixture('user.json')
      .then((user) => {
        cy.request({
          method: 'POST',
          url: 'http://localhost:5000/users/create',
          form: true,
          body: user
        }).then((response) => {
            uid = response.body._id.$oid
            name = user.firstName + ' ' + user.lastName
          })
        })
  })

  beforeEach(() => {
    cy.visit('http://localhost:5000/login')
  })

  //test case 1: open loginpage
  it('start out on the landing screen', () => {

    cy.get('h1').should('contain', 'Login')
  })

  //test case 2: login with correct credentials

  it('login with correct credentials', () => {
    cy.get('.inputwrapper #email').should('be.enabled')
    cy.get('.inputwrapper #password').should('be.disabled')
  })

  /*
  //clean up after test
  afterEach(() => {
    cy.request({
      method: 'DELETE',
      url: 'http://localhost:3000/user/' + uid,
    }).then((response) => {
      cy.log(response.body)
    })
  })
  */
})