package com.brunoxabreu.billing_orchestrator.service;

import com.brunoxabreu.billing_orchestrator.model.Subscription;
import com.stripe.Stripe;
import com.stripe.exception.StripeException;
import com.stripe.model.*;
import com.stripe.param.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@Slf4j
@Service
public class StripeService {

    @Value("${stripe.secret-key}")
    private String stripeSecretKey;

    public StripeService() {
        Stripe.apiVersion = "2023-10-16";
    }

    @Transactional
    public Subscription createSubscription(Subscription subscription) throws StripeException {
        Stripe.apiKey = stripeSecretKey;

        // Criar ou atualizar cliente no Stripe
        Customer customer = createOrUpdateCustomer(subscription);

        // Criar assinatura no Stripe
        SubscriptionCreateParams params = SubscriptionCreateParams.builder()
                .setCustomer(customer.getId())
                .setItems(SubscriptionCreateParams.Items.builder()
                        .setPrice(subscription.getPlanId())
                        .build())
                .setPaymentBehavior(SubscriptionCreateParams.PaymentBehavior.ERROR_IF_INCOMPLETE)
                .setPaymentSettings(SubscriptionCreateParams.PaymentSettings.builder()
                        .setPaymentMethodTypes(SubscriptionCreateParams.PaymentSettings.PaymentMethodTypes.builder()
                                .add("card")
                                .build())
                        .build())
                .setOffSession(SubscriptionCreateParams.OffSession.builder()
                        .setPaymentMethod(subscription.getPaymentMethodId())
                        .build())
                .build();

        com.stripe.model.Subscription stripeSubscription = com.stripe.model.Subscription.create(params);

        // Atualizar assinatura com dados do Stripe
        subscription.setStripeSubscriptionId(stripeSubscription.getId());
        subscription.setStatus(stripeSubscription.getStatus());
        subscription.setStartDate(LocalDateTime.ofEpochSecond(stripeSubscription.getStartDate(), 0, java.time.ZoneOffset.UTC));
        subscription.setNextBillingDate(LocalDateTime.ofEpochSecond(stripeSubscription.getCurrentPeriodEnd(), 0, java.time.ZoneOffset.UTC));

        return subscription;
    }

    @Transactional
    public Subscription updateSubscription(Subscription subscription) throws StriripeException {
        Stripe.apiKey = stripeSecretKey;

        com.stripe.model.Subscription stripeSubscription = com.stripe.model.Subscription.retrieve(subscription.getStripeSubscriptionId());

        // Atualizar assinatura no Stripe
        SubscriptionUpdateParams params = SubscriptionUpdateParams.builder()
                .setItems(SubscriptionUpdateParams.Items.builder()
                        .setPrice(subscription.getPlanId())
                        .build())
                .setProrationBehavior(SubscriptionUpdateParams.ProrationBehavior.ALWAYS_INVOICE)
                .build();

        stripeSubscription = stripeSubscription.update(params);

        // Atualizar assinatura com dados do Stripe
        subscription.setStatus(stripeSubscription.getStatus());
        subscription.setNextBillingDate(LocalDateTime.ofEpochSecond(stripeSubscription.getCurrentPeriodEnd(), 0, java.time.ZoneOffset.UTC));

        return subscription;
    }

    @Transactional
    public void cancelSubscription(String stripeSubscriptionId) throws StriripeException {
        Stripe.apiKey = stripeSecretKey;

        com.stripe.model.Subscription subscription = com.stripe.model.Subscription.retrieve(stripeSubscriptionId);
        subscription.cancel();
    }

    @Transactional
    public void reactivateSubscription(String stripeSubscriptionId) throws StriripeException {
        Stripe.apiKey = stripeSecretKey;

        com.stripe.model.Subscription subscription = com.stripe.model.Subscription.retrieve(stripeSubscriptionId);
        subscription.resume();
    }

    private Customer createOrUpdateCustomer(Subscription subscription) throws StriripeException {
        Map<String, Object> customerParams = new HashMap<>();
        customerParams.put("email", subscription.getCustomerId());
        customerParams.put("metadata", Map.of(
                "protheus_customer_id", subscription.getProtheusCustomerId()
        ));

        CustomerSearchParams params = CustomerSearchParams.builder()
                .setQuery("email:'" + subscription.getCustomerId() + "'")
                .build();

        CustomerSearchResult result = Customer.search(params);

        if (result.getData().isEmpty()) {
            return Customer.create(customerParams);
        } else {
            Customer customer = result.getData().get(0);
            return customer.update(customerParams);
        }
    }

    public Invoice retrieveInvoice(String invoiceId) throws StriripeException {
        Stripe.apiKey = stripeSecretKey;
        return Invoice.retrieve(invoiceId);
    }

    public PaymentIntent createPaymentIntent(BigDecimal amount, String currency) throws StriripeException {
        Stripe.apiKey = stripeSecretKey;

        PaymentIntentCreateParams params = PaymentIntentCreateParams.builder()
                .setAmount(amount.multiply(BigDecimal.valueOf(100)).longValue())
                .setCurrency(currency)
                .setAutomaticPaymentMethods(PaymentIntentCreateParams.AutomaticPaymentMethods.builder()
                        .setEnabled(true)
                        .build())
                .build();

        return PaymentIntent.create(params);
    }
} 