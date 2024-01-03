<script setup>
import CancelButton from "../buttons/CancelButton.vue";
import DeleteButton from "../buttons/DeleteButton.vue";
import MobileFullscreenDialog from "./MobileFullscreenDialog.vue";
</script>

<template>
  <ApolloMutation
    v-if="dialogOpen"
    :mutation="gqlMutation"
    :variables="{ ids: ids }"
    :update="update"
    @done="close(true)"
  >
    <template #default="{ mutate, loading, error }">
      <mobile-fullscreen-dialog v-model="dialogOpen">
        <template #title>
          <slot name="title">
            {{ $t("actions.confirm_deletion_multiple") }}
          </slot>
        </template>
        <template #content>
          <slot name="body">
            <ul class="text-body-1">
              <li v-for="(item, idx) in items" :key="idx">
                {{ nameOfItem(item) }}
              </li>
            </ul>
          </slot>
        </template>
        <template #actions>
          <cancel-button @click="close(false)" :disabled="loading">
            <slot name="cancelContent">
              <v-icon left>$cancel</v-icon>
              {{ $t("actions.cancel") }}
            </slot>
          </cancel-button>
          <delete-button @click="mutate" :loading="loading" :disabled="loading">
            <slot name="deleteContent" />
          </delete-button>
        </template>
      </mobile-fullscreen-dialog>
    </template>
  </ApolloMutation>
</template>

<script>
export default {
  name: "DeleteDialog",
  computed: {
    dialogOpen: {
      get() {
        return this.value;
      },

      set(val) {
        this.$emit("input", val);
      },
    },
    ids() {
      return this.items.map((item) => item[this.itemId]);
    },
    query() {
      if ("options" in this.gqlQuery) {
        return {
          ...this.gqlQuery.options,
          variables: JSON.parse(this.gqlQuery.previousVariablesJson),
        };
      }
      return { query: this.gqlQuery };
    },
  },
  methods: {
    update(store) {
      this.$emit("update", store);

      if (!this.gqlQuery) {
        // There is no GraphQL query to update
        return;
      }

      // Read the data from cache for query
      const storedData = store.readQuery(this.query);

      if (!storedData) {
        // There are no data in the cache yet
        return;
      }

      const storedDataKey = Object.keys(storedData)[0];

      for (const item of this.items) {
        console.debug("Removing item from store:", item);
        // Remove item from stored data
        const index = storedData[storedDataKey].findIndex(
          (m) => m.id === item.id,
        );
        storedData[storedDataKey].splice(index, 1);
      }

      // Write data back to the cache
      store.writeQuery({ ...this.query, data: storedData });
    },
    close(success) {
      this.$emit("input", false);
      if (success) {
        this.$emit("success");

        this.$root.snackbarItems.push({
          id: crypto.randomUUID(),
          timeout: 5000,
          messageKey: this.$t(this.deleteSuccessMessageI18nKey),
          color: "success",
        });
      } else {
        this.$emit("cancel");
      }
    },
    nameOfItem(item) {
      return this.itemAttribute in item || {}
        ? item[this.itemAttribute]
        : item.toString();
    },
  },
  props: {
    value: {
      type: Boolean,
      required: true,
    },
    items: {
      type: Array,
      required: false,
      default: () => [],
    },
    itemAttribute: {
      type: String,
      required: false,
      default: "name",
    },
    itemId: {
      type: String,
      required: false,
      default: "id",
    },
    gqlMutation: {
      type: Object,
      required: true,
    },
    gqlQuery: {
      type: Object,
      required: false,
      default: null,
    },
    deleteSuccessMessageI18nKey: {
      type: String,
      required: false,
      default: "status.objects_delete_success",
    },
  },
};
</script>
