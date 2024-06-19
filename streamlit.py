import streamlit as st

# Функция для расчета стоимости
def calculate_costs(num_docs, doc_size, storage_size, instance_type, s3_storage, users_per_day):
    instance_costs = {
        "t3.small.search": 26.28,
        "t3.medium.search": 53.29,
        "t2.micro.search": 13.14,
        "t2.small.search": 26.28,
        "t2.medium.search": 53.29,
        "m6g.large.search": 93.31,
        "m6g.xlarge.search": 186.62,
        "m6g.2xlarge.search": 372.96,
        "m6g.4xlarge.search": 746.88,
        "db.t3.small": 18.25,
        "db.t3.medium": 36.50,
        "db.r5.large": 91.98,
        "db.r5.xlarge": 183.96,
        "db.r5.2xlarge": 367.92,
    }

    # OpenSearch costs
    open_search_cost = instance_costs[instance_type] + (storage_size * 0.115)

    # RDS costs
    rds_cost = instance_costs[instance_type] + (storage_size * 0.115)

    # ECS costs (фиксированная конфигурация medium standard)
    ecs_vcpu_cost = 2 * 0.04048 * 24 * 30
    ecs_memory_cost = 4 * 0.004445 * 24 * 30
    ecs_cost = ecs_vcpu_cost + ecs_memory_cost

    # S3 costs
    s3_cost = s3_storage * 0.023

    # VPC costs (фиксированная стоимость)
    vpc_cost = 20.0  # Примерная фиксированная стоимость

    # Load Balancer costs (примерный расчет на основе количества пользователей в день)
    load_balancer_cost = users_per_day * 0.001  # Примерная стоимость за пользователя в день

    # Bastion Host costs (фиксированный тип инстанса, например, t3.micro)
    bastion_host_cost = 13.14  # Примерная стоимость за месяц для t3.micro

    total_cost = open_search_cost + rds_cost + ecs_cost + s3_cost + vpc_cost + load_balancer_cost + bastion_host_cost

    return open_search_cost, rds_cost, ecs_cost, s3_cost, vpc_cost, load_balancer_cost, bastion_host_cost, total_cost

# Функция для определения типа инстанса на основе размера документа
def determine_instance_type(num_docs, doc_size):
    storage_size = num_docs * doc_size / 1_000_000  # В GB
    if storage_size < 10:
        return "t2.micro.search"
    elif storage_size < 50:
        return "t3.small.search"
    elif storage_size < 200:
        return "t3.medium.search"
    elif storage_size < 500:
        return "m6g.large.search"
    elif storage_size < 1000:
        return "m6g.xlarge.search"
    elif storage_size < 2000:
        return "m6g.2xlarge.search"
    else:
        return "m6g.4xlarge.search"

# Заголовок приложения
st.title("AWS Cost Estimator")

# Ползунки для параметров
num_docs = st.slider("Number of Documents", 1_000, 3_000_000, step=1_000)
doc_size = st.slider("Document Size (KB)", 1, 1024, step=1)
storage_size = num_docs * doc_size / 1_000_000  # В GB

# Определение типа инстанса
instance_type = determine_instance_type(num_docs, doc_size)

s3_storage = st.slider("S3 Storage (GB)", 1, 10_000, step=1)
users_per_day = st.slider("Users per Day", 100, 100_000, step=100)

# Расчет стоимости
open_search_cost, rds_cost, ecs_cost, s3_cost, vpc_cost, load_balancer_cost, bastion_host_cost, total_cost = calculate_costs(
    num_docs, doc_size, storage_size, instance_type, s3_storage, users_per_day
)

# Отображение стоимости
st.subheader("Cost Breakdown")
st.write(f"OpenSearch Cost: ${open_search_cost:.2f}/month")
st.write(f"RDS Aurora PostgreSQL Cost: ${rds_cost:.2f}/month")
st.write(f"ECS Cost: ${ecs_cost:.2f}/month")
st.write(f"S3 Cost: ${s3_cost:.2f}/month")
st.write(f"VPC Cost: ${vpc_cost:.2f}/month")
st.write(f"Load Balancer Cost: ${load_balancer_cost:.2f}/month")
st.write(f"Bastion Host Cost: ${bastion_host_cost:.2f}/month")

st.subheader("Total Cost")
st.write(f"${total_cost:.2f}/month")
