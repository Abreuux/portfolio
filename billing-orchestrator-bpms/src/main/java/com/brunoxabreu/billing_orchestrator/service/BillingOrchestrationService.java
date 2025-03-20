package com.brunoxabreu.billing_orchestrator.service;

import com.brunoxabreu.billing_orchestrator.model.Subscription;
import io.camunda.zeebe.client.ZeebeClient;
import io.camunda.zeebe.client.api.response.ProcessInstanceEvent;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.HashMap;
import java.util.Map;

@Slf4j
@Service
public class BillingOrchestrationService {

    @Autowired
    private ZeebeClient zeebeClient;

    @Autowired
    private StripeService stripeService;

    @Autowired
    private ProtheusService protheusService;

    @Transactional
    public ProcessInstanceEvent startSubscriptionProcess(Subscription subscription) {
        log.info("Iniciando processo de assinatura para cliente: {}", subscription.getCustomerId());

        // Criar cliente no Protheus
        String protheusCustomerId = protheusService.createOrUpdateCustomer(subscription);
        subscription.setProtheusCustomerId(protheusCustomerId);

        // Criar assinatura no Stripe
        try {
            subscription = stripeService.createSubscription(subscription);
        } catch (Exception e) {
            log.error("Erro ao criar assinatura no Stripe: {}", e.getMessage());
            throw new RuntimeException("Erro ao criar assinatura no Stripe", e);
        }

        // Iniciar processo no Camunda
        Map<String, Object> variables = new HashMap<>();
        variables.put("subscriptionId", subscription.getId());
        variables.put("customerId", subscription.getCustomerId());
        variables.put("stripeSubscriptionId", subscription.getStripeSubscriptionId());
        variables.put("protheusCustomerId", subscription.getProtheusCustomerId());
        variables.put("amount", subscription.getAmount());
        variables.put("currency", subscription.getCurrency());
        variables.put("billingCycle", subscription.getBillingCycle());

        ProcessInstanceEvent processInstance = zeebeClient.newCreateInstanceCommand()
                .bpmnProcessId("billing-process")
                .latestVersion()
                .variables(variables)
                .send()
                .join();

        subscription.setProcessInstanceId(processInstance.getProcessInstanceKey().toString());
        return processInstance;
    }

    @Transactional
    public void handleSubscriptionUpdate(Subscription subscription) {
        log.info("Atualizando assinatura para cliente: {}", subscription.getCustomerId());

        try {
            // Atualizar no Stripe
            subscription = stripeService.updateSubscription(subscription);

            // Atualizar no Protheus
            protheusService.updateCustomerStatus(subscription.getProtheusCustomerId(), subscription.getStatus());

            // Enviar mensagem para o processo
            Map<String, Object> variables = new HashMap<>();
            variables.put("subscriptionId", subscription.getId());
            variables.put("status", subscription.getStatus());

            zeebeClient.newPublishMessageCommand()
                    .messageName("subscription-updated")
                    .correlationKey(subscription.getProcessInstanceId())
                    .variables(variables)
                    .send()
                    .join();

        } catch (Exception e) {
            log.error("Erro ao atualizar assinatura: {}", e.getMessage());
            throw new RuntimeException("Erro ao atualizar assinatura", e);
        }
    }

    @Transactional
    public void handleSubscriptionCancellation(Subscription subscription) {
        log.info("Cancelando assinatura para cliente: {}", subscription.getCustomerId());

        try {
            // Cancelar no Stripe
            stripeService.cancelSubscription(subscription.getStripeSubscriptionId());

            // Atualizar status no Protheus
            protheusService.updateCustomerStatus(subscription.getProtheusCustomerId(), "C");

            // Enviar mensagem para o processo
            Map<String, Object> variables = new HashMap<>();
            variables.put("subscriptionId", subscription.getId());
            variables.put("status", "cancelled");

            zeebeClient.newPublishMessageCommand()
                    .messageName("subscription-cancelled")
                    .correlationKey(subscription.getProcessInstanceId())
                    .variables(variables)
                    .send()
                    .join();

        } catch (Exception e) {
            log.error("Erro ao cancelar assinatura: {}", e.getMessage());
            throw new RuntimeException("Erro ao cancelar assinatura", e);
        }
    }

    @Transactional
    public void handlePaymentSuccess(String stripeInvoiceId, String protheusInvoiceId) {
        log.info("Processando pagamento bem-sucedido - Stripe: {}, Protheus: {}", 
                stripeInvoiceId, protheusInvoiceId);

        try {
            // Atualizar status da fatura no Protheus
            protheusService.updateInvoiceStatus(protheusInvoiceId, "P");

            // Enviar mensagem para o processo
            Map<String, Object> variables = new HashMap<>();
            variables.put("stripeInvoiceId", stripeInvoiceId);
            variables.put("protheusInvoiceId", protheusInvoiceId);
            variables.put("status", "paid");

            zeebeClient.newPublishMessageCommand()
                    .messageName("payment-success")
                    .correlationKey(protheusInvoiceId)
                    .variables(variables)
                    .send()
                    .join();

        } catch (Exception e) {
            log.error("Erro ao processar pagamento: {}", e.getMessage());
            throw new RuntimeException("Erro ao processar pagamento", e);
        }
    }

    @Transactional
    public void handlePaymentFailure(String stripeInvoiceId, String protheusInvoiceId) {
        log.info("Processando falha de pagamento - Stripe: {}, Protheus: {}", 
                stripeInvoiceId, protheusInvoiceId);

        try {
            // Atualizar status da fatura no Protheus
            protheusService.updateInvoiceStatus(protheusInvoiceId, "N");

            // Enviar mensagem para o processo
            Map<String, Object> variables = new HashMap<>();
            variables.put("stripeInvoiceId", stripeInvoiceId);
            variables.put("protheusInvoiceId", protheusInvoiceId);
            variables.put("status", "failed");

            zeebeClient.newPublishMessageCommand()
                    .messageName("payment-failure")
                    .correlationKey(protheusInvoiceId)
                    .variables(variables)
                    .send()
                    .join();

        } catch (Exception e) {
            log.error("Erro ao processar falha de pagamento: {}", e.getMessage());
            throw new RuntimeException("Erro ao processar falha de pagamento", e);
        }
    }
} 