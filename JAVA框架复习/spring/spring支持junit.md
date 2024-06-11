##### Spring支持junit的支持

* 首先学习spring对junit4的支持

  * 之前的测试举例

    ```java
    @Component
    public class Account {
        @Value(value = "张三")
        private String actno;
        @Value("123.0")
        private Double balance;
        public Account(String actno, Double balance) {
            this.actno = actno;
            this.balance = balance;
        }
        public Account() {
        }
        @Override
        public String toString() {
            return "Account{" +
                    "actno='" + actno + '\'' +
                    ", balance=" + balance +
                    '}';
        }
        public String getActno() {
            return actno;
        }
        public void setActno(String actno) {
            this.actno = actno;
        }
        public Double getBalance() {
            return balance;
        }
        public void setBalance(Double balance) {
            this.balance = balance;
        }
    }
    
    ```

    ```java
        @Test
        public void testIsolation2(){
            ApplicationContext applicationContext = new ClassPathXmlApplicationContext("spring.xml");
            Account account = applicationContext.getBean("account", Account.class);
            System.out.println(account);
        }
    ```

    

  * 使用spring之后，不用在加载配置文件

    ```java
    @RunWith(SpringJUnit4ClassRunner.class)
    @ContextConfiguration("classpath:spring.xml")
    //如果是全注解开发，使用
    //@ContextConfiguration(classes = SpringConfig.class)
    public class AccountTest {
        @Autowired
        private Account account;
        @Test
        public void testIsolation2(){
            System.out.println(account);
        }
    }
    ```

    

* spring对junit5的优化

  ```java
  @ExtendWith(SpringExtension.class)
  @ContextConfiguration("classpath:spring.xml")
  //如果是全注解开发，使用
  //@ContextConfiguration(classes = SpringConfig.class)
  public class AccountTest {
      @Autowired
      private Account account;
      @Test
      public void testIsolation2(){
          System.out.println(account);
      }
  }
  
  ```

  