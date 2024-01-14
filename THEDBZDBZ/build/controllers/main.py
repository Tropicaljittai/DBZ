from models.main import Model
from models.auth import Auth
from views.main import View

from .login import LogInController
from .signup import SignUpController
from .dashboard import DashboardController
from .accountDetails import AccountDetails_Controller
from .Products import productsController
from .variants import variantsController
from .orders import ordersController
from .createOrder import createOrder_Controller
from .customers import customersController
from .supply import supplyController
from .searchSupplier import searchSupplierController
from .orderSupply import orderSupply_Controller
class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.view = view
        self.model = model
        self.login_controller = LogInController(model, view)
        self.signup_controller = SignUpController(model, view)
        self.dashboardController = DashboardController(model,view)
        self.accountDetails_controller = AccountDetails_Controller(model,view)
        self.products_controller = productsController(model,view)
        self.variantsController = variantsController(model,view)
        self.ordersController = ordersController(model,view)
        self.createOrder_Controller = createOrder_Controller(model,view)
        self.customersController = customersController(model,view)
        self.supplyController = supplyController(model,view)
        self.searchSupplierController = searchSupplierController(model,view)
        self.orderSupply_Controller =orderSupply_Controller(model,view)
        
      
        # self.trigger_event("auth_changed")
        # self.trigger_event("finance_change")

        self.model.auth.add_event_listener(
            "auth_changed", self.auth_state_listener
        )
        # self.model.auth.add_event_listener(
        #     "finance_change", self.auth_state_listener
        # )


    def auth_state_listener(self, data):
        if data.is_logged_in:
            self.view.switch("dashboard")
            self.accountDetails_controller.update_view()
            self.model.auth.updateDashboard()
            self.products_controller.populate_treeview()
            self.createOrder_Controller.populate_treeview()
            self.customersController.populate_treeview()
            self.ordersController.populate_treeview()
            self.createOrder_Controller.createCustComboBox()
            self.ordersController.createComboBox()
            self.supplyController.createComboBox()
            self.supplyController.populateTreeView()
            self.searchSupplierController.populate_treeview()
    
            # self.model.auth.order_created() 
            # self.variantsController.populate_treeview()
            
    
        else:
            self.accountDetails_controller.clear()
            self.view.switch("login")



    # def finance_state_listener(self,info):
    #     if 


    def start(self):
        if self.model.auth.is_logged_in:
            self.view.switch("dashboard")
        else:
            self.view.switch("login")
        self.view.start_mainloop()

      