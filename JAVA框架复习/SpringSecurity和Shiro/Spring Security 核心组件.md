### SecurityContext

> `SecurityContext`是安全的上下文，所有的数据都是保存到SecurityContext中。

可以通过`SecurityContext`获取的对象有：

- Authentication

### SecurityContextHolder

> `SecurityContextHolder`用来获取SecurityContext中保存的数据的工具。通过使用静态方法获取SecurityContext的相对应的数据。

```java
SecurityContext context = SecurityContextHolder.getContext();
```

### Authentication

> Authentication表示当前的认证情况，可以获取的对象有：
>
> UserDetails：获取用户信息，是否锁定等额外信息。
>
> Credentials：获取密码。
>
> isAuthenticated：获取是否已经认证过。
>
> Principal：获取用户，如果没有认证，那么就是用户名，如果认证了，返回UserDetails。

### UserDetails

```csharp
public interface UserDetails extends Serializable {

	Collection<? extends GrantedAuthority> getAuthorities();
	String getPassword();
	String getUsername();
	boolean isAccountNonExpired();
	boolean isAccountNonLocked();
	boolean isCredentialsNonExpired();
	boolean isEnabled();
}
```

### UserDetailsService

> UserDetailsService可以通过loadUserByUsername获取UserDetails对象。该接口供spring security进行用户验证。
>
> 通常使用自定义一个CustomUserDetailsService来实现UserDetailsService接口，通过自定义查询UserDetails。

### AuthenticationManager

> AuthenticationManager用来进行验证，如果验证失败会抛出相对应的异常。

### PasswordEncoder

> 密码加密器。通常是自定义指定。
>
> BCryptPasswordEncoder：哈希算法加密
>
> NoOpPasswordEncoder：不使用加密





## spring security session 无状态支持权限控制(前后分离)

> spring security会在默认的情况下将认证信息放到HttpSession中。
>
> 但是对于我们的前后端分离的情况，如app，小程序，web前后分离等，httpSession就没有用武之地了。这时我们可以通过`configure(httpSecurity)`设置spring security是否使用httpSession。

```scala
@Configuration
public class MySecurityConfiguration extends WebSecurityConfigurerAdapter {
    // code...
    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http
                .sessionManagement()
            	//设置无状态，所有的值如下所示。
                .sessionCreationPolicy(SessionCreationPolicy.STATELESS)
                // code...
    }
    // code...
}
```

共有四种值，其中默认的是ifRequired。

- ***always*** – a session will always be created if one doesn’t already exist，没有session就创建。
- ***ifRequired*** – a session will be created only if required (**default**)，如果需要就创建（默认）。
- ***never*** – the framework will never create a session itself but it will use one if it already exists
- ***stateless*** – no session will be created or used by Spring Security 不创建不使用session

> 由于前后端不通过保存session和cookie来进行判断，所以为了保证spring security能够记录登录状态，所以需要传递一个值，让这个值能够自我验证来源，同时能够得到数据信息。选型我们选择[JWT](https://www.cnblogs.com/dl610455894/p/JWT.md)。对于java客户端我们选择使用[jjwt](https://github.com/jwtk/jjwt)。