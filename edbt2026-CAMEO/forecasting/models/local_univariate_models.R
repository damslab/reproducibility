# Implementations of a set of univariate forecasting models
#
# Each function takes 2 parameters
# time_series - a ts object representing the time series that should be used with model training
# forecast_horizon - expected forecast horizon
#
# If a model fails to provide forecasts, it will return snaive forecasts
# Code reproduced from https://github.com/rakshitha123/TSForecasting/blob/master/models/local_univariate_models.R


# Calculate ets forecasts
get_ets_forecasts <- function(time_series, forecast_horizon){
    model <- forecast::ets(time_series, seasonal.periods = seasonal_periods)
    f <- forecast::forecast(model, h = forecast_horizon)$mean
    list(f, coef(model))
}

get_stlf_forecasts <- function(time_series, forecast_horizon){
    model <- forecast::stlf(time_series, method="ets")
    f <- forecast::forecast(model, h = forecast_horizon)$mean
}


get_stlf_arima_forecasts <- function(time_series, forecast_horizon){
    set.seed(42)
    model <- forecast::stlf(time_series, method="arima")
    f <- forecast::forecast(model, h = forecast_horizon)$mean
}

# Calculate simple exponential smoothing forecasts
get_ses_forecasts <- function(time_series, forecast_horizon){
  tryCatch(
    forecast(forecast::ses(time_series, h = forecast_horizon))$mean
  , error = function(e) {
    warning(e)
    get_snaive_forecasts(time_series, forecast_horizon)
  })
}


# Calculate theta forecasts
get_theta_forecasts <-function(time_series, forecast_horizon){
  forecast::thetaf(y = time_series, h = forecast_horizon)$mean
}


# Calculate auto.arima forecasts
get_arima_forecasts <- function(time_series, forecast_horizon, model = NULL){
  if(is.null(model)){
    tryCatch({
        print('Called auto normal arima')
        fit <- forecast:::auto.arima(time_series, lambda = 'auto', stepwise=FALSE, parallel=TRUE)
    }, error = function(e) {
        tryCatch({
          print('Failed: Calling auto normal arima without lambda')
          fit <<- forecast:::auto.arima(time_series, seasonal = FALSE, stepwise=FALSE, parallel=TRUE)
        }, error = function(e){
            fit <<- forecast:::auto.arima(time_series, seasonal = FALSE)
        })
    })

    tryCatch({
      f <- forecast:::forecast.Arima(fit, h = forecast_horizon)$mean
      list(f, fit)
    }, error = function(e) {
        warning(e)
        f <- get_snaive_forecasts(time_series, forecast_horizon)
        list(f, fit)
    })
  }else{
    tryCatch({
      print("Computing ARIMA without training")
      f <- forecast::forecast(forecast:::Arima(time_series, model = model), h = forecast_horizon)$mean
    }, error = function(e) {
        warning(e)
        f <- get_snaive_forecasts(time_series, forecast_horizon)
    })
  }
}


# Calculate tbats forecasts
get_tbats_forecasts <- function(time_series, forecast_horizon){
  tryCatch(
    forecast(forecast::tbats(time_series), h = forecast_horizon)$mean
  , error = function(e) {
    warning(e)
    get_snaive_forecasts(time_series, forecast_horizon)
  })
}


# Calculate dynamic harmonic regression arima forecasts
get_dhr_arima_forecasts <- function(time_series, forecast_horizon, ar_order = NULL){

  if(is.null(ar_order)){
      print('Called auto arima')
      xreg <- forecast::fourier(time_series, K = c(1,1))
      model <- forecast::auto.arima(time_series, xreg = xreg, seasonal = FALSE)
      xreg1 <- forecast::fourier(time_series, K = c(1,1), h = forecast_horizon)
      f <- forecast::forecast(model, xreg = xreg1)$mean
      list(f, model$arma[c(1, 6, 2)])
  }else{
    print(paste("Called Arima with order", paste(ar_order, collapse = " ")))
    xreg <- forecast::fourier(time_series, K = c(1,1))
    xreg1 <- forecast::fourier(time_series, K = c(1,1), h = forecast_horizon)
    tryCatch({
        f <- forecast::forecast(forecast::Arima(time_series, order = ar_order, xreg = xreg), xreg = xreg1)$mean
        list(f, ar_order)
    }, error = function(e){
        print("Warning: arima model failed due to stationary reasons")
        print("Computing new ARMA order")
        xreg <- forecast::fourier(time_series, K = c(1,1))
        model <- forecast::auto.arima(time_series, xreg = xreg, seasonal = FALSE)
        xreg1 <- forecast::fourier(time_series, K = c(1,1), h = forecast_horizon)
        f <- forecast::forecast(model, xreg = xreg1)$mean
        print(paste("New model computed with order", paste(model$arma[c(1, 6, 2)], collapse = " ")))
        list(f, model$arma[c(1, 6, 2)])
    })
  }
}


# Calculate snaive forecasts
get_snaive_forecasts <- function(time_series, forecast_horizon){
  forecast::snaive(time_series, h = forecast_horizon)$mean
}
