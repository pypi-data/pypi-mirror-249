<script setup>
import CancelButton from "../buttons/CancelButton.vue";
import DeleteButton from "../buttons/DeleteButton.vue";
import MobileFullscreenDialog from "./MobileFullscreenDialog.vue";
</script>

<template>
  <ApolloMutation
    v-if="dialogOpen"
    :mutation="gqlMutation"
    :variables="{ id: item.id }"
    :update="update"
    @done="close(true)"
  >
    <template #default="{ mutate, loading, error }">
      <mobile-fullscreen-dialog v-model="dialogOpen">
        <template #title>
          <slot name="title">
            {{ $t("actions.confirm_deletion") }}
          </slot>
        </template>
        <template #content>
          <slot name="body">
            <p class="text-body-1">{{ nameOfObject }}</p>
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
      <v-snackbar :value="error !== null">
        {{ error }}

        <template #action="{ attrs }">
          <v-btn color="primary" text v-bind="attrs" @click="error = null" icon>
            <v-icon>$close</v-icon>
          </v-btn>
        </template>
      </v-snackbar>
    </template>
  </ApolloMutation>
</template>

<script>
export default {
  name: "DeleteDialog",
  computed: {
    nameOfObject() {
      return this.itemAttribute in this.item || {}
        ? this.item[this.itemAttribute]
        : this.item.toString();
    },
    dialogOpen: {
      get() {
        return this.value;
      },

      set(val) {
        this.$emit("input", val);
      },
    },
    query() {
      if (this.gqlQuery && "options" in this.gqlQuery) {
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

      // Remove item from stored data
      const index = storedData[storedDataKey].findIndex(
        (m) => m.id === this.item.id,
      );
      storedData[storedDataKey].splice(index, 1);

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
  },
  props: {
    value: {
      type: Boolean,
      required: true,
    },
    item: {
      type: Object,
      required: false,
      default: () => ({}),
    },
    itemAttribute: {
      type: String,
      required: false,
      default: "name",
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
      default: "status.object_delete_success",
    },
  },
};
</script>
